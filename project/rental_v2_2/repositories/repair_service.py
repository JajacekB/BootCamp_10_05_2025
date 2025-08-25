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
        new_period = (today - rental.start_date).days
        new_total_cost = rental.total_cost * new_period / old_period

        invoice = self.session.query(Invoice).filter(Invoice.rental_id == rental.id).first()

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

    def finish_after_vehicle_swap(self, vehicle: Vehicle, replacement_vehicle: Vehicle, rental: RentalHistory, different_price: bool):
        today = date.today()
        old_rental = rental
        old_rental_cost = old_rental.total_cost
        old_rental_period = (old_rental.planned_return_date - old_rental.start_date).days
        real_rental_days_old = max((today - old_rental.start_date).days, 1)
        real_rental_days_new = max((old_rental.planned_return_date - today).days, 0)

        broken_veh_cost = old_rental_cost * real_rental_days_old / old_rental_period

        if different_price:
            user = self.session.query(User).filter(User.id == vehicle.user_id).first()
            replacement_full_cost, _, _ = calculate_rental_cost(
                self.session, user, replacement_vehicle.cash_per_day, old_rental_period
            )
            replacement_veh_cost = replacement_full_cost * real_rental_days_new / old_rental_period
        else:
            replacement_veh_cost = old_rental_cost - broken_veh_cost

        vehicle.is_available = True
        vehicle.borrower_id = None
        vehicle.return_date = None

        replacement_vehicle.is_available = False
        replacement_vehicle.borrower_id = rental.user_id
        replacement_vehicle.return_date = rental.planned_return_date

        old_rental.actual_return_date = today
        old_rental.total_cost = round(broken_veh_cost, 2)

        base_res_id = old_rental.reservation_id
        existing = self.session.query(RentalHistory).filter(
            RentalHistory.reservation_id.like(f"{base_res_id}%")
        ).all()
        new_suffix = chr(65 + len(existing))
        new_res_id = f"{base_res_id}{new_suffix}"

        new_rental = RentalHistory(
            reservation_id=new_res_id,
            user_id=old_rental.user_id,
            vehicle_id=replacement_vehicle.id,
            start_date=today,
            planned_return_date=old_rental.planned_return_date,
            base_cost=round(replacement_veh_cost, 2),
            total_cost=round(replacement_veh_cost, 2),
        )

        self.session.add(new_rental)
        return {
            "replacement_vehicle": replacement_vehicle,
            "new_rental": new_rental,
            "broken_veh_cost": broken_veh_cost
        }

    def finalize_repair(self, vehicle: Vehicle, work_user, planned_return_date, total_cost, description):
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

        return repair