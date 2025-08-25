# repair_service.py
from datetime import date
from collections import defaultdict

from models.user import User
from models.vehicle import Vehicle
from models.invoice import Invoice
from models.repair_history import RepairHistory
from models.rental_history import RentalHistory
from services.id_generators import generate_repair_id
from services.rental_costs import calculate_rental_cost
from services.vehicle_avability import get_available_vehicles, get_unavailable_vehicle


class RepairService:
    def __init__(self, session):
        self.session = session

    def get_filtered_vehicles(self, status: str, vehicle_type: str):

        if status == "Dostępne":
            vehicles = get_available_vehicles(self.session, vehicle_type=vehicle_type)

        elif status == "Niedostępne":
            vehicles, _ = get_unavailable_vehicle(self.session, vehicle_type=vehicle_type)

        else:
            if vehicle_type == "all":
                vehicles = self.session.query(Vehicle).all()

            else:
                vehicles = self.session.query(Vehicle).filter(Vehicle.type == vehicle_type).all()

        if not vehicles:
            print("\n🚫 Brak pasujących pojazdów.")
            return

        vehicles_sorted = sorted(
            vehicles, key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model, v.individual_id)
        )

        grouped = defaultdict(list)
        for v in vehicles_sorted:
            key = (v.brand, v.vehicle_model, v.cash_per_day)
            grouped[key].append(v)

        return grouped

    def finish_broken_rental(self, vehicle: Vehicle):
        """Zakończenie wynajmu pojazdu popsutego (bez commita)."""
        today = date.today()

        rental = self.session.query(RentalHistory).filter(
            RentalHistory.vehicle_id == vehicle.id,
            RentalHistory.actual_return_date == None
        ).first()

        if not rental:
            return None, None

        old_period = (rental.planned_return_date - rental.start_date).days
        new_period = max(1, (today - rental.start_date).days)
        new_total_cost = rental.total_cost * new_period / old_period

        invoice = self.session.query(Invoice).filter(Invoice.rental_id == rental.id).first()

        print(f"{new_total_cost=}")
        print(f"{invoice=}")

        vehicle.is_available = True
        vehicle.borrower_id = None
        vehicle.return_date = None

        rental.actual_return_date = today
        rental.total_cost = new_total_cost

        if invoice:
            invoice.amount = new_total_cost
            self.session.add(invoice)

        self.session.add_all([vehicle, rental])

        return rental, invoice

    def finish_after_vehicle_swap(self, broken_vehicle: Vehicle, replacement_vehicle: Vehicle,
                                  old_rental: RentalHistory, different_price: bool):
        """
        Obsługa podmiany pojazdu:
        - broken_vehicle -> warsztat (naprawa)
        - replacement_vehicle -> klient na resztę okresu wynajmu
        - old_rental: obecny rental popsutego pojazdu
        - different_price: True -> liczymy proporcjonalnie do ceny nowego pojazdu
        """
        today = date.today()

        # 🔹 Zamiana statusu starego pojazdu
        broken_vehicle.is_available = False
        broken_vehicle.borrower_id = None  # klient zwraca
        broken_vehicle.return_date = old_rental.planned_return_date

        # 🔹 Zakończenie starego rentalu
        old_rental.actual_return_date = today
        old_rental.total_cost = old_rental.total_cost  # zostawiamy jak było
        self.session.add(old_rental)
        self.session.add(broken_vehicle)

        # 🔹 Konfiguracja nowego rentalu dla zastępczego pojazdu
        rental_days_remaining = (old_rental.planned_return_date - today).days
        rental_days_remaining = max(rental_days_remaining, 1)

        if different_price:
            new_total_cost = replacement_vehicle.cash_per_day * rental_days_remaining
        else:
            # koszt liczony po starej cenie pojazdu
            new_total_cost = old_rental.base_cost * rental_days_remaining

        replacement_vehicle.is_available = False
        replacement_vehicle.borrower_id = old_rental.user_id
        replacement_vehicle.return_date = old_rental.planned_return_date
        self.session.add(replacement_vehicle)

        new_res_id = old_rental.reservation_id + "_R"  # np. nowy suffix
        new_rental = RentalHistory(
            reservation_id=new_res_id,
            user_id=old_rental.user_id,
            vehicle_id=replacement_vehicle.id,
            start_date=today,
            planned_return_date=old_rental.planned_return_date,
            base_cost=old_rental.base_cost,
            total_cost=new_total_cost
        )
        self.session.add(new_rental)

        return {
            "broken_vehicle": broken_vehicle,
            "replacement_vehicle": replacement_vehicle,
            "old_rental": old_rental,
            "new_rental": new_rental,
            "total_cost_new": new_total_cost
        }

    def finalize_repair(self, vehicle: Vehicle, work_user, planned_return_date, total_cost, description):
        print("🔧 finalize repair")
        repair_id = generate_repair_id(self.session)
        repair = RepairHistory(
            repair_id=repair_id,
            vehicle_id=vehicle.id,
            mechanic_id=work_user.id,
            start_date=date.today(),
            planned_return_date=planned_return_date,
            cost=total_cost,
            description=description
        )
        self.session.add(repair)

        vehicle.is_available = False
        vehicle.borrower_id = work_user.id
        vehicle.return_date = planned_return_date

        # self.session.commit()

        print("Utworzono nowy object RepairHistory")
        return repair