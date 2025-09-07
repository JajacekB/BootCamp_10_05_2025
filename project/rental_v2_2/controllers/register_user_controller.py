from PySide6.QtWidgets import QMessageBox

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


    def on_registration_finished_widget(self, user):

        success, text = add_user(self.session, user)

        if success:
            if self.admin_dialog:
                QMessageBox.information(self.view, "Sukces", text)
                self.admin_dialog.clear_dynamic_area()
            else:
                self.view.close()
        else:
            QMessageBox.warning(self.view, "Niepowodzenie", text)

    def on_get_sellers_count(self):
        print("Emit działa")
        sellers = get_user_by(self.session, only_one=False, role="seller")
        count = len(sellers)

        seller_number = str(count + 1).zfill(2)
        seller_login = f"Seller{seller_number}"
        raw_password = seller_login
        print(f"\nUtworzono login: {seller_login} | hasło: {raw_password}")
        self.view.populate_auto_seller(seller_login, raw_password)

    def on_registration_cancelled_widget(self):
        print("❌ Rejestracja anulowana – czyszczenie dynamicznego obszaru (RegisterWidget).")
        self.view.clear_form()
