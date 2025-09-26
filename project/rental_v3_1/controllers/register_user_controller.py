from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Slot
import bcrypt

from models.user import User
from repositories.write_methods import add_user
from repositories.read_methods import get_user_by


class RegisterUserController:


    def __init__(self, session, view, parent_dialog=None):
        self.session = session
        self.view = view
        self.admin_dialog = parent_dialog
        self.view.controller = self
        self.view.registration_finished.connect(self.on_registration_finished_widget)
        self.view.registration_cancelled.connect(self.on_registration_cancelled_widget)
        self.view.handle_login_password.connect(self.on_get_sellers_count)

    @Slot(dict)
    def on_registration_finished_widget(self, user_data):

        password_hash = bcrypt.hashpw(
            user_data["password"].encode("utf-8"),
            bcrypt.gensalt()
        ).decode()

        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            login=user_data["login"],
            phone=user_data["phone"],
            email=user_data["email"],
            password_hash=password_hash,
            address=user_data["address"],
            role=user_data["role"],
        )

        success, text = add_user(self.session, new_user)

        self.view.show_success(success, text)

    def on_get_sellers_count(self, role):
        print("Emit działa")
        if role == "seller":
            sellers = get_user_by(self.session, only_one=False, role="seller")
            count = len(sellers)

            seller_number = str(count + 1).zfill(2)
            staff_login = f"Seller{seller_number}"
        elif role == "accountant":
            accountant = get_user_by(self.session, only_one=False, role="accountant")
            count = len(accountant)

            accountant_number = str(count + 1).zfill(2)
            staff_login = f"Accountant{accountant_number}"

        raw_password = staff_login
        print(f"\nUtworzono login: {staff_login} | hasło: {raw_password}")
        self.view.populate_auto_seller(staff_login, raw_password)

    def on_registration_cancelled_widget(self):
        print("❌ Rejestracja anulowana – czyszczenie dynamicznego obszaru (RegisterWidget).")
        self.view.clear_form()
