# delete_users_service.py
from models.user import User
from models.vehicle import Vehicle


class DeleteUsersService:
    def __init__(self, session, role="client"):
        self.session = session
        self.role = role

    def get_candidates(self):
        """Zwraca listę kandydatów do usunięcia."""
        active_renters_ids = {
            v.borrower_id
            for v in self.session.query(Vehicle.borrower_id)
            .filter(Vehicle.is_available == False, Vehicle.borrower_id != None)
            .distinct()
        }

        candidates = self.session.query(User).filter(
            User.id.notin_(active_renters_ids),
            User.role == self.role,
            User.is_active == True
        ).all()

        return [
            {"id": u.id, "first_name": u.first_name, "last_name": u.last_name, "login": u.login}
            for u in candidates
        ]

    def get_user_details(self, uid):
        user = self.session.query(User).filter(User.id == uid).first()
        if not user:
            return None

        if user.role == "seller":
            return (
                f"Czy chcesz usunąć?\n\n"
                f"Pracownik wypożyczalni: {user.first_name} {user.last_name}\n"
                f"email: {user.email}\n"
                f"zamieszkały: {user.address}\n"
                f"login: {user.login}"
            )
        else:
            return (
                f"Czy chcesz usunąć?\n\n"
                f"Użytkownik: {user.first_name} {user.last_name}\n"
                f"email: {user.email}\n"
                f"zamieszkały: {user.address}\n"
                f"login: {user.login}"
            )

    def deactivate_user(self, uid):
        user = self.session.query(User).filter(User.id == uid).first()
        if not user:
            return False

        user.is_active = False
        self.session.commit()
        return True