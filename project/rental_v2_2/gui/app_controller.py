import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QObject, Signal, Qt

from database.base import SessionLocal, Session

from gui.windows.start_window import StartWindow
from gui.windows.login_dialog import LoginDialog
from gui.windows.register_dialog import RegisterWindow
from gui.windows.admin_dialog import AdminDialog
from gui.windows.seller_dialog import SellerDialog
from gui.windows.client_dialog import ClientDialog

from services.overdue_check import check_overdue_vehicles
from services.user_service import add_seller, add_client,remove_user, get_clients, update_profile
from services.vehicle_management import add_vehicles_batch, remove_vehicle, get_vehicle
from services.rental_process import rent_vehicle_for_client, return_vehicle
from services.repair import repair_vehicle



class UserLoggedInSignal(QObject):

    loggedIn = Signal(object)


class AppController(QObject):

    loggedOut = Signal()

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)

        self.current_user = None
        self.db_session: Session = None

        try:
            self.db_session = SessionLocal()
            print("✅ Początkowa sesja bazy danych otwarta w kontrolerze.")
        except Exception as e:
            print(f"❌ Błąd podczas otwierania początkowej sesji bazy danych: {e}")
            sys.exit(1)

        self.app.aboutToQuit.connect(self._close_db_session_on_exit)

        self.start_window = StartWindow()
        self.register_window = None

        self.start_window.login_requested.connect(self._handle_login_request)
        self.start_window.register_requested.connect(self._handle_register_request)

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


    def _handle_register_request(self):
        print("\n--- Obsługa żądania rejestracji z GUI ---")

        self.register_window = RegisterWindow()
        self.register_window.registration_finished.connect(self._on_registration_finished)

        self.register_window.show()
        self.current_active_window = self.register_window


    def _on_registration_finished(self, success: bool):
        if success:
            print("Rejestracja zakończona sukcesem, wracam do StartWindow")
        else:
            print("Rejestracja nieudana, wracam do StartWindow")

        if self.register_window:
            self.register_window.close()
            self.register_window = None

        self.start_window.show()
        self.current_active_window = self.start_window


    def _on_user_logged_in(self, user):
        print(f"Kontroler: Użytkownik {user.first_name} {user.last_name} ({user.role}) zalogowany. Przechodzę do menu.")

        self.current_user = user
        # Call a method to show the appropriate menu based on user role, passing the persistent session
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

        # Sprawdzenie zaległości — tylko dla admina i sprzedawcy
        if user.role in ("seller", "admin"):
            try:
                check_overdue_vehicles(self.db_session, user)
            except Exception as e:
                print(f"❌ Błąd podczas sprawdzania zaległości: {e}")

        # GUI menu dla każdej roli
        if user.role == "admin":
            self._show_admin_menu()

        elif user.role == "seller":
            self._show_seller_menu()

        elif user.role == "client":
            self._show_seller_menu()

        else:
            print(f"❌ Nieznana rola użytkownika: {user.role}")
            self._handle_logout_request()


    def _handle_admin_command(self, command_num: str):
        commands = {
            "1": lambda: add_seller(self.db_session),
            "2": lambda: remove_user(self.db_session, role="seller"),
            "3": lambda: add_client(self.db_session),
            "4": lambda: remove_user(self.db_session),
            "5": lambda: get_clients(self.db_session),

            "6": lambda: add_vehicles_batch(self.db_session),
            "7": lambda: remove_vehicle(self.db_session),
            "8": lambda: get_vehicle(self.db_session),

            "9": lambda: rent_vehicle_for_client(self.db_session, self.current_user),
            "10": lambda: return_vehicle(self.db_session, self.current_user),
            "11": lambda: repair_vehicle(self.db_session),

            "12": lambda: update_profile(self.db_session, self.current_user)
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
        self.admin_dialog.setWindowModality(Qt.ApplicationModal)
        self.admin_dialog.show()
        self.admin_dialog.raise_()
        self.admin_dialog.activateWindow()
        self.current_active_window = self.admin_dialog


    def _handle_seller_command(self, command_num: str):
        commands = {
            "1": lambda: add_client(self.db_session),
            "2": lambda: remove_user(self.db_session),
            "3": lambda: get_clients(self.db_session),

            "4": lambda: add_vehicles_batch(self.db_session),
            "5": lambda: remove_vehicle(self.db_session),
            "6": lambda: get_vehicle(self.db_session),

            "7": lambda: rent_vehicle_for_client(self.db_session, self.current_user),
            "8": lambda: return_vehicle(self.db_session, self.current_user),
            "9": lambda: repair_vehicle(self.db_session),

            "10": lambda: update_profile(self.db_session, self.current_user)
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
        self.seller_dialog.command_selected.connect(self._handle_seller_command)
        self.seller_dialog.setWindowModality(Qt.ApplicationModal)
        self.seller_dialog.show()
        self.seller_dialog.raise_()
        self.seller_dialog.activateWindow()
        self.current_active_window = self.seller_dialog


    def _handle_client_command(self, command_num: str):
        commands = {
            "1": lambda: get_vehicle(self.db_session),
            "2": lambda: rent_vehicle_for_client(self.db_session, self.current_user),
            "3": lambda: return_vehicle(self.db_session, self.current_user),
            "4": lambda: update_profile(self.db_session, self.current_user)
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
        self.client_dialog.command_selected.connect(self._handle_client_command)
        self.client_dialog.setWindowModality(Qt.ApplicationModal)
        self.client_dialog.show()
        self.client_dialog.raise_()
        self.client_dialog.activateWindow()
        self.current_active_window = self.client_dialog


