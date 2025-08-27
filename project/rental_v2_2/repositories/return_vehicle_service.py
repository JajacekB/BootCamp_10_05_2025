# repositories.return_vehicle_service.py
from models.rental_history import RentalHistory



class ReturnVehicleService:
    def __init__(self, session, user = None):
        self.session = session
        self.user = user

    def get_rentals_from_db(self, mode):

        active_rentals = self.session.query(RentalHistory).filter(
            RentalHistory.user_id == self.user.id,
            RentalHistory.actual_return_date.is_(None)
        ).order_by(RentalHistory.planned_return_date.desc()).all()

        historical_rentals = self.session.query(RentalHistory).filter(
            RentalHistory.user_id == self.user.id,
            RentalHistory.actual_return_date.isnot(None)
        ).order_by(RentalHistory.planned_return_date.desc()).all()

        if mode == "Aktywne":
            return active_rentals
        elif mode == "Historyczne":
            return historical_rentals
        else:
            return active_rentals + [None] + historical_rentals