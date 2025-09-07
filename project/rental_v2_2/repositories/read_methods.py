# repositories/read_methods.py
from datetime import date
from sqlalchemy import func

from models.user import User
from models.vehicle import Vehicle
from models.promotions import Promotion
from models.rental_history import RentalHistory
from models.repair_history import RepairHistory
from services.vehicle_avability import get_available_vehicles


def get_replacement_vehicle(session, reference_vehicle, planned_return_date, prefer_cheaper: bool):

    available_vehicles = get_available_vehicles(
        session, date.today(), planned_return_date, reference_vehicle.type
    )

    if prefer_cheaper:

        vehicle = next(
            (v for v in sorted(available_vehicles, key=lambda v: v.cash_per_day, reverse=True)
            if v.cash_per_day < reference_vehicle.cash_per_day),
            None
        )
    else:

        vehicle = next(
            (v for v in sorted(available_vehicles, key=lambda v: v.cash_per_day)
            if v.cash_per_day > reference_vehicle.cash_per_day),
            None
        )

    return vehicle

def get_rental_for_vehicle(session, vehicle_id, planned_return_date):

    today = date.today()
    rental = session.query(RentalHistory).filter(
        RentalHistory.vehicle_id == vehicle_id,
        func.date(RentalHistory.start_date) <= planned_return_date,
        func.date(RentalHistory.planned_return_date) >= today
    ).first()

    return rental

def get_vehicle_by_id(session, vehicle_id):

    return session.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).one_or_none()

def get_user_by(session, only_one: bool=True, **kwargs):
    allowed_keys = {
        "user_id": User.id,
        "user_login": User.login,
        "email": User.email,
        "role": User.role}

    if len(kwargs) != 1:
        raise ValueError("Podaj dokładnie jeden parametr: user_id, user_login albo email")

    key, value = next(iter(kwargs.items()))

    if key not in allowed_keys:
        raise ValueError(f"Niepoprawny parametr: {key}. Dozwolone: {list(allowed_keys.keys())}")

    column = allowed_keys[key]
    query = session.query(User).filter(column == value)

    if only_one:
        return query.one_or_none()
    else:
        return query.all()


def get_rentals_by_vehicle_id(session, vehicle):
    return list(
        session.query(RentalHistory)
        .filter(RentalHistory.vehicle_id == vehicle.id)
        .order_by(RentalHistory.planned_return_date)
        .all()
    )


def get_repairs_by_vehicle_id(session, vehicle):
    return list(
        session.query(RepairHistory)
        .filter(RepairHistory.vehicle_id == vehicle.id)
        .order_by(RepairHistory.planned_return_date)
        .all()
    )


def promo_banner_data(session):
    time_promos = session.query(Promotion).filter_by(type='time').order_by(Promotion.min_days).all()
    loyalty_promos = session.query(Promotion).filter_by(type='loyalty').all()

    return time_promos, loyalty_promos


def overdue_tasks(session):
    today = date.today()

    rentals = (
        session.query(RentalHistory)
        .filter(RentalHistory.planned_return_date < today,
                RentalHistory.actual_return_date == None)
        .all()
    )

    repairs = (
        session.query(RepairHistory)
        .filter(RepairHistory.planned_return_date < today,
                RepairHistory.actual_return_date == None)
        .all()
    )
    return [
        {
            "type": "rental",
            "id_number": r.reservation_id,
            "brand": r.vehicle.brand,
            "model": r.vehicle.vehicle_model,
            "vehicle_type": getattr(r.vehicle, "type", ""),
            "start_date": r.start_date,
            "end_date": r.actual_return_date or r.planned_return_date,
            "cost": r.total_cost,
            "obj": r,
        }
        for r in rentals
    ] + [
        {
            "type": "repair",
            "id_number": rp.repair_id,
            "brand": rp.vehicle.brand,
            "model": rp.vehicle.vehicle_model,
            "vehicle_type": getattr(rp.vehicle, "type", ""),
            "start_date": rp.start_date,
            "end_date": rp.actual_return_date or rp.planned_return_date,
            "cost": rp.cost,
            "obj": rp,
        }
        for rp in repairs
    ]