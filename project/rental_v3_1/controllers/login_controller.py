# controllers/login_controller.py
from services.auth_service import login_user

class LoginController:
    def login_user(self, data: dict):
        login = data.get("login")
        password = data.get("password")
        user = login_user(login, password)
        if user:
            return True, f"Zalogowano jako {user.first_name}", user
        return False, "Nieprawidłowy login/email lub hasło", None
