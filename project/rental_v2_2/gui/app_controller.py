import sys
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox

from database.base import SessionLocal #, Session

from gui.windows.start_window import StartWindow
from gui.windows.login_window import LoginDialog
from gui.windows.admin_dialog import AdminDialog
from gui.windows.seller_dialog import SellerDialog
from gui.windows.client_dialog import ClientDialog
from gui.windows.register_wiget import RegisterWidget
from gui.windows.get_users_widget import GetUsersWidget
from gui.windows.get_vehicle_widget import GetVehicleWidget
from gui.windows.add_vehicle_widget import AddVehicleWidget
from gui.windows.update_user_widget import UpdateUserWidget
from gui.windows.rent_vehicle_widget import RentVehicleWidget
from gui.windows.delete_client_widget import DeleteUsersWidget
from gui.windows.return_vehicle_widget import ReturnVehicleWidget
from gui.windows.remove_vehicle_widget import RemoveVehicleWidget
from gui.windows.repair_vehicle_widget import RepairVehicleWidget
from gui.windows.overdue_rentals_widget import OverdueRentalsWidget

from services.repair import repair_vehicle
from services.user_service import update_profile
from services.rental_process import rent_vehicle_for_client, return_vehicle, rent_vehicle



class UserLoggedInSignal(QObject):

    loggedIn = Signal(object)


class AppController(QObject):
    clear_requested = Signal()
    loggedOut = Signal()

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.start_window = None
        self.login_window = None
        self.admin_dialog = None
        self.register_widget = None
        self.register_window_parent = None
        self.current_active_window = None


        self.current_user = None
        self.db_session: SessionLocal = None

        try:
            self.db_session = SessionLocal()
            print("✅ Początkowa sesja bazy danych otwarta w kontrolerze.")
        except Exception as e:
            print(f"❌ Błąd podczas otwierania początkowej sesji bazy danych: {e}")
            sys.exit(1)

        self.app.aboutToQuit.connect(self._close_db_session_on_exit)

        self.start_window = StartWindow()
        self.register_widget = None

        self.start_window.login_requested.connect(self._handle_login_request)
        self.start_window.register_requested.connect(self._handle_register_window)

        self.loggedOut.connect(self._show_start_window)

        self.user_logged_in_signal = UserLoggedInSignal()
        self.user_logged_in_signal.loggedIn.connect(self._on_user_logged_in)

        self.current_active_window: QWidget = None


    def run(self):
        self._show_start_window()
        sys.exit(self.app.exec())


    def _show_start_window(self):
        if self.current_active_window:
            self.current_active_window.hide()
        self.start_window.show()
        self.current_active_window = self.start_window


    def _handle_login_request(self):
        print("\n--- Obsługa żądania logowania z GUI ---")

        login_dialog = LoginDialog(self.db_session, self.start_window)
        login_dialog.login_successful.connect(self._on_user_logged_in)

        login_dialog.login_cancelled.connect(self._show_start_window)

        login_dialog.exec()

        print("--- Proces logowania w GUI zakończony ---")


    def _handle_add_seller_wiget(self):
        print("\n--- Dodawanie sprzedawcy (auto login/hasło) ---")

        self.register_widget = RegisterWidget(
            session=self.db_session,
            parent=self.start_window,
            role="seller",
            auto=True
        )
        self.register_widget.registration_finished.connect(self.on_registration_finished_widget)
        self.register_widget.registration_cancelled.connect(self.on_registration_cancelled_widget)

        self.admin_dialog.show_register_widget(role="seller", auto=True)

        print("--- Proces dodawania sprzedawcy zakończony ---")


    def _handle_register_window(self):
        """Wyświetla rejestrację jako osobne okno (np. z poziomu StartWindow)."""
        self.register_widget = RegisterWidget(self.db_session)
        self.register_widget.registration_finished.connect(self.on_registration_finished_widget)
        self.register_widget.registration_cancelled.connect(self.on_registration_cancelled_widget)
        self.register_widget.show()


    def handle_register_widget(self):
        if self.admin_dialog is None:
            print("❌ Błąd: AdminDialog nie został zainicjalizowany.")
            return

        self.register_widget = RegisterWidget(self.db_session)
        self.register_widget.registration_finished.connect(self.on_registration_finished_widget)
        self.register_widget.registration_cancelled.connect(self.on_registration_cancelled_widget)
        self.admin_dialog.show_register_widget(self.register_widget)


    def on_registration_finished_widget(self, success: bool):
        if success:
            QMessageBox.information(None, "Sukces", "Użytkownik został zarejestrowany.")
        else:
            QMessageBox.warning(None, "Niepowodzenie", "Rejestracja nie powiodła się.")

        if self.admin_dialog:
            self.admin_dialog.clear_dynamic_area()


    def on_registration_cancelled_widget(self):
        print("❌ Rejestracja anulowana – czyszczenie dynamicznego obszaru (RegisterWidget).")
        self.register_widget.clear_form()


    def _on_user_logged_in(self, user):
        print(f"Kontroler: Użytkownik {user.first_name} {user.last_name} ({user.role}) zalogowany. Przechodzę do menu.")

        self.current_user = user
        self._show_main_user_menu(user)


    def _handle_logout_request(self):
        print("\n🔒 Wylogowano. Zamykam sesję bazy danych.")

        self.current_user = None
        self.loggedOut.emit()


    def logout(self):
        self._handle_logout_request()


    def _close_db_session_on_exit(self):
        if self.db_session:
            self.db_session.close()
            print("✅ Sesja bazy danych zamknięta podczas zamykania aplikacji.")
        self.db_session = None


    def _show_main_user_menu(self, user):
        if not self.db_session:
            print("❌ Błąd: Brak aktywnej sesji bazy danych dla zalogowanego użytkownika.")
            self.loggedOut.emit()
            return

        print(f"Wyświetlam menu dla roli: {user.role}")

        if user.role == "admin":
            self._show_admin_menu()

        elif user.role == "seller":
            self._show_seller_menu()

        elif user.role == "client":
            self._show_client_menu()

        else:
            print(f"❌ Nieznana rola użytkownika: {user.role}")
            self._handle_logout_request()


    def _handle_admin_command(self, command_num: str):
        commands = {
            "1": lambda: self._handle_add_seller_wiget(),
            "2": lambda: self.show_delete_seller_widget(),
            "3": lambda: self.handle_register_widget(),
            "4": lambda: self.show_delete_client_widget(),
            "5": lambda: self.show_get_users_widget(),

            "6": lambda: self.show_add_vehicle_widget(),
            "7": lambda: self.show_remove_vehicle_widget(),
            "8": lambda: self.show_get_vehicle_widget(),

            "9": lambda: self.show_rent_vehicle_widget(),
            "10": lambda: self.show_return_vehicle_widget(),
            "11": lambda: self.show_repair_vehicle_widget(),

            "12": lambda: self.show_update_user_widget()
        }
        action = commands.get(command_num)
        if action:
            action()
        else:
            print(f"❌ Nieznana komenda: {command_num}")


    def _show_admin_menu(self):
        if self.current_active_window:
            self.current_active_window.close()

        self.admin_dialog = AdminDialog(
            user=self.current_user,
            session=self.db_session,
            controller=self
        )
        self.admin_dialog.command_selected.connect(self._handle_admin_command)
        self.admin_dialog.logout.connect(self.logout)

        self.admin_dialog.showMaximized()
        self.admin_dialog.raise_()
        self.admin_dialog.activateWindow()
        self.current_active_window = self.admin_dialog


    def _handle_seller_command(self, command_num: str):
        commands = {
            "1": lambda: self.handle_register_widget(),
            "2": lambda: self.show_delete_client_widget(),
            "3": lambda: self.show_get_vehicle_widget(),

            "4": lambda: self.show_add_vehicle_widget(),
            "5": lambda: self.show_remove_vehicle_widget(),
            "6": lambda: self.show_get_vehicle_widget(),

            "7": lambda: self.show_rent_vehicle_widget(),
            "8": lambda: self.show_return_vehicle_widget(),
            "9": lambda: self.show_repair_vehicle_widget(),

            "10": lambda: self.show_update_user_widget()
        }
        action = commands.get(command_num)
        if action:
            action()
        else:
            print(f"❌ Nieznana komenda: {command_num}")


    def _show_seller_menu(self):
        if self.current_active_window:
            self.current_active_window.close()

        self.seller_dialog = SellerDialog(
            user=self.current_user,
            session=self.db_session,
            controller=self
        )
        self.seller_dialog.logout.connect(self.logout)
        self.seller_dialog.command_selected.connect(self._handle_seller_command)

        self.seller_dialog.showMaximized()
        self.seller_dialog.raise_()
        self.seller_dialog.activateWindow()
        self.current_active_window = self.seller_dialog


    def _handle_client_command(self, command_num: str):
        commands = {
            "1": lambda: self.show_get_vehicle_widget(),
            "2": lambda: self.show_rent_vehicle_widget(),
            "3": lambda: self.show_return_vehicle_widget(),
            "4": lambda: self.show_update_user_widget()
        }
        action = commands.get(command_num)
        if action:
            action()
        else:
            print(f"❌ Nieznana komenda: {command_num}")


    def _show_client_menu(self):
        if self.current_active_window:
            self.current_active_window.close()

        self.client_dialog = ClientDialog(
            user=self.current_user,
            session=self.db_session,
            controller=self
        )
        self.client_dialog.logout.connect(self.logout)
        self.client_dialog.command_selected.connect(self._handle_client_command)

        self.client_dialog.showMaximized()
        self.client_dialog.raise_()
        self.client_dialog.activateWindow()
        self.current_active_window = self.client_dialog

    def show_get_vehicle_widget(self):
        print("🔧🔧🔧 Wywołano show_get_vehicle_widget()")
        self.get_vehicle_widget = GetVehicleWidget(self.db_session)
        self.show_widget(self.get_vehicle_widget)

    def show_get_users_widget(self):
        print("🔧🔧🔧 Wywołano show_get_users_widget()")
        self.get_users_widget = GetUsersWidget(self.db_session)
        self.show_widget(self.get_users_widget)

    def show_delete_client_widget(self):
        print("🔧🔧🔧 Wywołano delete_client_widget()")
        self.delete_client_widget = DeleteUsersWidget(self.db_session)
        self.show_widget(self.delete_client_widget)

    def show_delete_seller_widget(self):
        print("🔧🔧🔧 Wywołano delete_client_widget()")
        self.delete_client_widget = DeleteUsersWidget(self.db_session, "seller")
        self.show_widget(self.delete_client_widget)

    def show_add_vehicle_widget(self):
        print("🔧🔧🔧 Wywołano add_vehicle_widget()")
        self.add_vehicle_widget = AddVehicleWidget(self.db_session)
        self.show_widget(self.add_vehicle_widget)

    def show_remove_vehicle_widget(self):
        print("🔧🔧🔧 Wywołano remove_vehicle_widget()")
        self.remove_vehicle_widget = RemoveVehicleWidget(self.db_session)
        self.show_widget(self.remove_vehicle_widget)

    def show_rent_vehicle_widget(self):
        print("🔧🔧🔧 Wywołano rent_vehicle_widget()")
        self.rent_vehicle_widget = RentVehicleWidget(self.db_session, self.current_user)
        self.show_widget(self.rent_vehicle_widget)

    def show_return_vehicle_widget(self):
        print("🔧🔧🔧 Wywołano return_vehicle_widget()")
        self.return_vehicle_widget = ReturnVehicleWidget(self.db_session, self.current_user)
        self.show_widget(self.return_vehicle_widget)

    def show_overdue_rentals_widget(self):
        print("🔧🔧🔧 Uruchomiono overdue_rentals_widget()")
        self.overdue_vehicle_rentals = OverdueRentalsWidget(self.db_session, self.current_user)
        self.show_widget(self.overdue_vehicle_rentals)

    def show_repair_vehicle_widget(self):
        print("🔧🔧🔧 Uruchomiono repair_vehicle_widget()")
        self.repair_vehicle_widget = RepairVehicleWidget(self.db_session, self.current_user)
        self.show_widget(self.repair_vehicle_widget)

    def show_update_user_widget(self):
        print("🔧🔧🔧 Uruchomiono update_user_widget()")
        self.update_user_widget = UpdateUserWidget(self.db_session, self.current_user)
        self.show_widget(self.update_user_widget)

    def show_widget(self, widget: QWidget):
        if self.current_active_window and hasattr(self.current_active_window, "dynamic_area"):
            layout = self.current_active_window.dynamic_area.layout()
            # Wyczyść dynamiczny obszar
            for i in reversed(range(layout.count())):
                widget_to_remove = layout.itemAt(i).widget()
                if widget_to_remove is not None:
                    widget_to_remove.setParent(None)

            layout.addWidget(widget)
            widget.show()
            print("✅ Widget został dodany do dynamicznego obszaru.")
        else:
            print("❌ Nie można znaleźć dynamicznego obszaru do wyświetlenia widgetu.")


