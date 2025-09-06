# get_users_service.py
from collections import defaultdict
from sqlalchemy import desc
from models.user import User
from models.vehicle import Vehicle
from models.rental_history import RentalHistory

class GetUsersService:
    def __init__(self, session):
        self.session = session

    def get_users_with_rent(self):

        vehicles = self.session.query(Vehicle).filter(Vehicle.is_available == False).all()
        if not vehicles:
            return []
        user_ids = [v.borrower_id for v in vehicles if v.borrower_id is not None]
        return (
            self.session.query(User)
            .filter(User.id.in_(user_ids), User.role == "client")
            .order_by(User.last_name, User.first_name)
            .all()
        )

    def get_users_without_rent(self):

        vehicles = self.session.query(Vehicle).filter(Vehicle.is_available == False).all()
        user_ids = [v.borrower_id for v in vehicles] if vehicles else []
        return (
            self.session.query(User)
            .filter(User.id.notin_(user_ids), User.role == "client", User.is_active == True)
            .order_by(User.last_name, User.first_name)
            .all()
        )

    def get_all_clients(self):

        active = (
            self.session.query(User)
            .filter(User.role == "client", User.is_active == True)
            .order_by(User.last_name, User.first_name)
            .all()
        )
        inactive = (
            self.session.query(User)
            .filter(User.role == "client", User.is_active == False)
            .order_by(User.first_name, User.last_name)
            .all()
        )
        return active + inactive

    def get_inactive_users(self):

        return (
            self.session.query(User)
            .filter(User.role == "client", User.is_active == False)
            .order_by(User.first_name, User.last_name)
            .all()
        )

    def format_users(self, users):
        """Tworzy czytelne stringi do wyświetlenia w liście."""
        user_view = defaultdict(list)
        for u in users:
            key = (u.id, u.first_name, u.last_name, u.login)
            user_view[key].append(u)
        return [
            (uid, f"ID: [{uid:03d}]  -  {first} {last},  login: {login}.")
            for (uid, first, last, login) in user_view
        ]

    def get_user_details(self, user_id: int) -> dict:
        """Zwraca dane o użytkowniku i ostatnim wypożyczeniu"""
        user = self.session.query(User).filter_by(id=user_id).first()
        vehicle = self.session.query(Vehicle).filter_by(borrower_id=user_id).first()
        active_rentals = self.session.query(RentalHistory).filter(
            RentalHistory.user_id == user_id,
            RentalHistory.actual_return_date.is_(None)
        ).order_by(RentalHistory.planned_return_date.desc()).all()

        historical_rentals = self.session.query(RentalHistory).filter(
            RentalHistory.user_id == user_id,
            RentalHistory.actual_return_date.isnot(None)
        ).order_by(RentalHistory.planned_return_date.desc()).all()

        rentals = active_rentals + historical_rentals


        # rent = (
        #     self.session.query(RentalHistory)
        #     .filter_by(user_id=user_id)
        #     .order_by(desc(RentalHistory.planned_return_date))
        #     .first()
        # )
        return {
            "user": user,
            "vehicle": vehicle if vehicle else None,
            "rent": rentals if rentals else None,
        }