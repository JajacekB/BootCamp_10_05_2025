import sys
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from database import SessionLocal
from gui.windows.start_window import StartWindow
from gui.windows.login_window import LoginDialog
from gui.windows.admin_dialog import AdminDialog
from controllers.admin_dialog_controller import AdminDialogController
from gui.widgets.register_user_view import RegisterUserView
from controllers.register_user_controller import RegisterUserController


class StartWindowController(QObject):

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.start_window = StartWindow()
        self.db_session: SessionLocal = None
        self.current_user = None
        self.current_active_window = None
        self.admin_dialog_controller: AdminDialogController = None

        self.start_window.login_requested.connect(self._handle_login_request)
        self.start_window.register_requested.connect(self._handle_register_request)
        self.start_window.quit_requested.connect(self._handle_quit)

        self._open_db_session()
        self._show_start_window()

    def run(self):
        sys.exit(self.app.exec())

    def _open_db_session(self):
        try:
            self.db_session = SessionLocal()
            print("✅ Sesja bazy danych otwarta")
        except Exception as e:
            print(f"❌ Błąd otwarcia sesji DB: {e}")
            sys.exit(1)

    def _close_db_session(self):
        if self.db_session:
            self.db_session.close()
            print("✅ Sesja bazy danych zamknięta")
            self.db_session = None

    def _show_start_window(self):
        if self.current_active_window:
            self.current_active_window.hide()
        self.start_window.show()
        self.current_active_window = self.start_window

    def _handle_login_request(self):
        login_dialog = LoginDialog(self.db_session, self.start_window)
        login_dialog.login_successful.connect(self._on_user_logged_in)
        login_dialog.login_cancelled.connect(self._show_start_window)
        login_dialog.exec()

    def _on_user_logged_in(self, user):
        self.current_user = user
        self.current_role = user.role
        print(f"Step 1 {self.current_user=}, {self.current_role=}")
        self._show_admin_dialog()

    def _show_admin_dialog(self):
        if self.current_active_window:
            self.current_active_window.hide()
        print(f"Step 2 {self.current_user=}, {self.current_role=}")

        self.admin_dialog_controller = AdminDialogController(
            user=self.current_user,
            db_session=self.db_session,
            parent_window=self.start_window,
            logout_callback=self._on_user_logged_out
        )
        self.admin_dialog_controller.show()
        self.current_active_window = self.admin_dialog_controller.dialog

    def _on_user_logged_out(self):
        self.current_user = None
        self._show_start_window()

    def _handle_register_request(self):
        if self.start_window is None:
            print("❌ Błąd: StartWindow nie został zainicjalizowany.")
            return
        self.view = RegisterUserView(parent=self.start_window, role="client", auto=False)
        controller = RegisterUserController(self.db_session, self.view, parent_dialog=None)
        self.controller = controller

        self.view.exec()

    def _handle_quit(self):
        self._close_db_session()
        self.start_window.handle_exit_program()
        # self.app.quit()


