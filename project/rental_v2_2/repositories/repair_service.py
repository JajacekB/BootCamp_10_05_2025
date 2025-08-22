from datetime import date
from sqlalchemy.orm import Session

from models.user import User
from models.invoice import Invoice
from models.vehicle import Vehicle
from models.repair_history import RepairHistory
from models.rental_history import RentalHistory
from services.id_generators import generate_repair_id
from services.rental_costs import calculate_rental_cost



def finish_broken_rental(session: Session, vehicle: Vehicle):
    """
    Zakończenie wynajmu pojazdu popsutego (bez commita).
    """
    today = date.today()

    # Pobierz aktywny najem dla pojazdu
    rental = session.query(RentalHistory).filter(
        RentalHistory.vehicle_id == vehicle.id,
        RentalHistory.actual_return_date == None  # tylko aktualny
    ).first()

    if not rental:
        print("Nie znależiono aktualnego wynajmu")
        pass
        return None, None

    old_period = (rental.planned_return_date - rental.start_date).days
    new_period = (today - rental.start_date).days
    new_total_cost = rental.total_cost * new_period / old_period

    invoice = session.query(Invoice).filter(Invoice.rental_id == rental.id).first()

    # Aktualizacja statusu pojazdu
    vehicle.is_available = True
    vehicle.borrower_id = None
    vehicle.return_date = None

    # Aktualizacja historii najmu
    rental.actual_return_date = today
    rental.total_cost = new_total_cost

    if invoice:
        invoice.amount = new_total_cost
        session.add(invoice)

    session.add_all([vehicle, rental])

    print("Zakończono stary rental")

    # nic nie commitujemy tutaj
    return rental, invoice


def finish_after_vehicle_swap(session, vehicle, replacement_vehicle, rental, different_price: bool):
    today = date.today()

    old_rental = rental
    old_rental_cost = old_rental.total_cost
    old_rental_period = (old_rental.planned_return_date - old_rental.start_date).days
    real_rental_days_old = max((today - old_rental.start_date).days, 1)
    real_rental_days_new = max((old_rental.planned_return_date - today).days, 0)

    # koszt pojazdu zepsutego
    broken_veh_cost = old_rental_cost * real_rental_days_old / old_rental_period

    # koszt pojazdu zastępczego
    if different_price:
        user = session.query(User).filter(User.id == vehicle.user_id).first()
        replacement_full_cost, _, _ = calculate_rental_cost(
            session, user, replacement_vehicle.cash_per_day, old_rental_period
        )
        replacement_veh_cost = replacement_full_cost * real_rental_days_new / old_rental_period
    else:
        replacement_veh_cost = old_rental_cost - broken_veh_cost

    # Aktualizacja statusów pojazdów
    vehicle.is_available = True
    vehicle.borrower_id = None
    vehicle.return_date = None

    replacement_vehicle.is_available = False
    replacement_vehicle.borrower_id = rental.user_id
    replacement_vehicle.return_date = rental.planned_return_date

    # Aktualizacja historii najmu popsutego pojazdu
    old_rental.actual_return_date = today
    old_rental.total_cost = round(broken_veh_cost, 2)

    # Nowa rezerwacja dla pojazdu zastępczego
    base_res_id = old_rental.reservation_id
    existing = session.query(RentalHistory).filter(
        RentalHistory.reservation_id.like(f"{base_res_id}%")
    ).all()
    new_suffix = chr(65 + len(existing))  # 'A', 'B', 'C'...
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

    session.add(new_rental)
    print("Dodanao nowy obiekt do RentalHistory ")

    # zwracamy dane do GUI, ale nie commitujemy
    return {
        "replacement_vehicle": replacement_vehicle,
        "new_rental": new_rental,
        "broken_veh_cost": broken_veh_cost
    }


def finalize_repair(session, vehicle, work_user, planned_return_date, total_cost, description):
    """
    Finalny commit całego procesu (jedyny commit w module).
    """
    print("🔧 finalize repair")

    repair_id = generate_repair_id(session)

    repair = RepairHistory(
        repair_id=repair_id,
        vehicle_id=vehicle.id,
        mechanic_id=work_user.id,
        start_date=date.today(),
        planned_return_date=planned_return_date,
        cost=total_cost,
        description=description
    )
    session.add(repair)

    vehicle.is_available = False
    vehicle.borrower_id = work_user.id
    vehicle.return_date = planned_return_date

    print("Utworzono nowy object RepairHistory")