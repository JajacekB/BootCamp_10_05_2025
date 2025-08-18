# repositories/get_methods.py
from models.rental_history import RentalHistory
from sqlalchemy import func
from datetime import date

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