from datetime import date
from sqlalchemy.orm import Session

from models.user import User
from models.invoice import Invoice
from models.vehicle import Vehicle
from models.repair_history import RepairHistory
from models.rental_history import RentalHistory
from services.id_generators import generate_repair_id
from services.rental_costs import calculate_rental_cost


def finalize_repair(session, vehicle, work_user, planned_return_date, total_cost, description):
    print("🔧 step 5a")

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

    try:
        session.commit()
        return repair  # 👈 zwróć obiekt naprawy (albo np. tuple z danymi do wyświetlenia)
    except Exception as e:
        session.rollback()
        raise e  # 👈 GUI decyduje jak pokazać błąd


def finish_after_vehicle_swap(session, vehicle, replacement_vehicle, different_price: bool):
    today = date.today()

    old_rental = vehicle.rental
    old_rental_cost = old_rental.total_cost
    old_rental_period = (old_rental.planned_return_date - old_rental.start_date).days
    real_rental_days_old = max((today - old_rental.start_date).days, 1)
    real_rental_days_new = max((old_rental.planned_return_date - today).days, 0)

    # koszt pojazdu zepsutego
    broken_veh_cost = old_rental_cost * real_rental_days_old / old_rental_period

    # koszt pojazdu zastępczego
    if different_price:
        user = session.query(User).filter(User.id == vehicle.user_id).first()
        replacement_full_cost, _, _ = calculate_rental_cost(user, replacement_vehicle.cash_per_day, old_rental_period)
        replacement_veh_cost = replacement_full_cost * real_rental_days_new / old_rental_period
    else:
        replacement_veh_cost = old_rental_cost - broken_veh_cost

    # Aktualizacja statusów pojazdów
    vehicle.is_available = True
    vehicle.borrower_id = None
    vehicle.return_date = None

    replacement_vehicle.is_available = False
    replacement_vehicle.borrower_id = vehicle.rental.user_id
    replacement_vehicle.return_date = vehicle.rental.planned_return_date

    # Aktualizacja historii najmu popsutego pojazdu
    old_rental.actual_return_date = today
    old_rental.total_cost = round(broken_veh_cost, 2)

    # Nowa rezerwacja dla pojazdu zastępczego
    base_res_id = old_rental.reservation_id
    existing = session.query(RentalHistory).filter(RentalHistory.reservation_id.like(f"{base_res_id}%")).all()
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
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    # zwracamy dane do GUI
    return {
        "replacement_vehicle": replacement_vehicle,
        "new_rental": new_rental,
        "broken_veh_cost": broken_veh_cost
    }


def finish_broken_rental(session: Session, vehicle: Vehicle):
    """
    Zakończenie wynajmu pojazdu popsutego, aktualizacja bazy danych.
    Zwraca RentalHistory i ewentualnie Invoice po aktualizacji.
    """
    today = date.today()
    rental = vehicle.rental_history  # zakładamy, że vehicle.rental jest dostępne

    old_period = (rental.planned_return_date - rental.start_date).days
    new_period = (today - rental.start_date).days
    new_total_cost = rental.total_cost * new_period / old_period

    invoice = session.query(Invoice).filter(Invoice.rental_id == rental.id).first()
    if not invoice:
        return None, None  # brak faktury

    # Aktualizacja statusu pojazdu
    vehicle.is_available = True
    vehicle.borrower_id = None
    vehicle.return_date = None

    # Aktualizacja historii najmu
    rental.actual_return_date = today
    rental.total_cost = new_total_cost

    invoice.amount = new_total_cost

    try:
        session.add_all([vehicle, rental, invoice])
        session.commit()
        return rental, invoice
    except Exception as e:
        session.rollback()
        raise e