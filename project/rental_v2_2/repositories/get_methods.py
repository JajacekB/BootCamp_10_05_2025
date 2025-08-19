# repositories/get_methods.py

from services.vehicle_avability import get_available_vehicles
from models.vehicle import Vehicle
from models.rental_history import RentalHistory
from sqlalchemy import func
from datetime import date


def find_replacement_vehicle(session, reference_vehicle, planned_return_date, prefer_cheaper: bool):
    # szukanie pojazdu z flagą preffer_cheeper
    available_vehicles = get_available_vehicles(
        session, date.today(), planned_return_date, reference_vehicle.type
    )

    if prefer_cheaper:
        # Najdroższy z tańszych
        vehicle = next(
            (v for v in sorted(available_vehicles, key=lambda v: v.cash_per_day, reverse=True)
            if v.cash_per_day < reference_vehicle.cash_per_day),
            None
        )
    else:
        # Najtańszy z droższych
        vehicle = next(
            (v for v in sorted(available_vehicles, key=lambda v: v.cash_per_day)
            if v.cash_per_day > reference_vehicle.cash_per_day),
            None
        )

    return vehicle

def get_rental_for_vehicle(session, vehicle_id, planned_return_date):
    """
    Zwraca aktualną rezerwację dla pojazdu w podanym okresie.
    Zwraca obiekt RentalHistory lub None.
    """
    today = date.today()
    rental = session.query(RentalHistory).filter(
        RentalHistory.vehicle_id == vehicle_id,
        func.date(RentalHistory.start_date) <= planned_return_date,
        func.date(RentalHistory.planned_return_date) >= today
    ).first()
    return rental

def get_vehicle_by_id(session, vehicle_id):
    """Zwraca pojazd po ID lub None."""
    return session.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).one_or_none()