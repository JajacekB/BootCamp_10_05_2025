import sys
from PySide6.QtWidgets import QApplication, QWidget # QWidget for potential future main menus
from PySide6.QtCore import QObject, Signal

# Import backend services and database session
from database.base import SessionLocal, Session # Import Session for type hinting
from services.user_service import register_user
from services.auth_service import login_user, login_user_gui # Import both for now, use login_user_gui

# Import your GUI windows
from gui.windows.start_window import StartWindow # Assuming StartWindow is now in gui/windows/
from gui.windows.login_dialog import LoginDialog # NEW: Import LoginDialog

# Import menu functions (these are still console-based, will be replaced by GUI)
from ui.menu_admin import menu_admin
from ui.menu_seller import menu_seller
from ui.menu_client import menu_client
from services.overdue_check import check_overdue_vehicles

# Define a custom signal for when a user successfully logs in
class UserLoggedInSignal(QObject):
    # Signal that emits a user object (e.g., models.user.User instance)
    loggedIn = Signal(object)

# This class will manage the overall flow of your GUI application
class AppController(QObject):
    # Define a signal that can be emitted when a user logs out
    # This can be used to reset the UI to the initial state
    loggedOut = Signal()

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)

        # Main application state variables
        self.current_user = None  # Stores the logged-in user object
        self.db_session: Session = None # Will hold the active database session

        # Open the initial database session here, as requested by the user.
        # This session will be used for login and registration, and then for the logged-in user.
        try:
            self.db_session = SessionLocal()
            print("✅ Początkowa sesja bazy danych otwarta w kontrolerze.")
        except Exception as e:
            print(f"❌ Błąd podczas otwierania początkowej sesji bazy danych: {e}")
            # Handle critical error, e.g., show an error message and exit the application
            sys.exit(1)

        # Ensure the session is closed when the application quits
        self.app.aboutToQuit.connect(self._close_db_session_on_exit)

        # Initialize windows
        self.start_window = StartWindow()
        # You'll add more windows here as your app grows (e.g., self.login_dialog, self.main_menu_window)

        # Connect signals from StartWindow to controller methods
        self.start_window.login_requested.connect(self._handle_login_request)
        self.start_window.register_requested.connect(self._handle_register_request)

        # Connect the controller's loggedOut signal to a method that shows the start window
        self.loggedOut.connect(self._show_start_window)

        # Connect login success signal (for internal use, e.g., showing user-specific menu)
        self.user_logged_in_signal = UserLoggedInSignal()
        self.user_logged_in_signal.loggedIn.connect(self._on_user_logged_in)

        # Keep track of the current active GUI window/widget (e.g., StartWindow, AdminMenu, etc.)
        self.current_active_window: QWidget = None

    def run(self):
        """
        Starts the application by showing the initial window and entering the event loop.
        """
        self._show_start_window() # Start by showing the initial window
        sys.exit(self.app.exec())

    def _show_start_window(self):
        """
        Shows the StartWindow and hides any other active window.
        """
        if self.current_active_window:
            self.current_active_window.hide()
        self.start_window.show()
        self.current_active_window = self.start_window

    def _handle_login_request(self):
        """
        Handles the login request from the StartWindow.
        Opens the LoginDialog and handles its result.
        The StartWindow remains visible in the background.
        """
        print("\n--- Obsługa żądania logowania z GUI ---")
        # Removed: self.start_window.hide() to keep StartWindow visible

        # Create and show the LoginDialog
        # Set StartWindow as parent so LoginDialog appears on top of it
        login_dialog = LoginDialog(self.db_session, self.start_window)
        login_dialog.login_successful.connect(self._on_user_logged_in)
        # If cancelled, the LoginDialog will simply close, and StartWindow remains visible
        login_dialog.login_cancelled.connect(self._show_start_window)

        # Show the dialog modally (blocks until closed)
        login_dialog.exec()

        print("--- Proces logowania w GUI zakończony ---")


    def _handle_register_request(self):
        """
        Handles the registration request from the StartWindow.
        Uses the controller's persistent database session for the registration process.
        NOTE: This still uses the console-based register_user for now.
        """
        print("\n--- Rozpoczynanie procesu rejestracji (proszę sprawdzić konsolę) ---")
        # Ensure the session is open before using it
        if not self.db_session:
            try:
                self.db_session = SessionLocal()
                print("✅ Sesja bazy danych ponownie otwarta dla rejestracji.")
            except Exception as e:
                print(f"❌ Błąd podczas ponownego otwierania sesji dla rejestracji: {e}")
                return # Cannot proceed without a session

        user = register_user(self.db_session) # Use the controller's persistent session
        if user:
            print(f"Zarejestrowano nowego użytkownika: {user.first_name} {user.last_name} ({user.login}) (Rola: {user.role})")
            # Optionally, automatically log in the new user or prompt them to log in
            # For now, we'll just print.
        else:
            print("Rejestracja nieudana.")
        print("--- Proces rejestracji zakończony ---")

    def _on_user_logged_in(self, user):
        """
        Callback executed when a user successfully logs in.
        This is where you'd transition from the StartWindow/LoginDialog to the main application menu.
        """
        print(f"Kontroler: Użytkownik {user.first_name} {user.last_name} ({user.role}) zalogowany. Przechodzę do menu.")
        # Hide the window that triggered the login (could be StartWindow or LoginDialog)
        if self.current_active_window:
            self.current_active_window.hide()
        # Set the current user
        self.current_user = user
        # Call a method to show the appropriate menu based on user role, passing the persistent session
        self._show_main_user_menu(user)

    def _show_main_user_menu(self, user):
        """
        Shows the main application menu based on the user's role.
        This will eventually involve creating and showing different QWidgets/QMainWindows.
        For now, it will print to console and simulate backend checks.
        """
        if not self.db_session:
            print("❌ Błąd: Brak aktywnej sesji bazy danych dla zalogowanego użytkownika.")
            self.loggedOut.emit() # Force logout if no session
            return

        print(f"Wyświetlam menu dla roli: {user.role}")

        # Simulate backend checks that would normally happen in main.py
        if user.role in ("seller", "admin"):
            print("Sprawdzam zaległe pojazdy...")
            check_overdue_vehicles(self.db_session, user) # Use the persistent session

        # This part still uses your console-based menu functions.
        # In a full GUI app, you'd instantiate and show a new QWidget/QMainWindow here
        # (e.g., AdminMenu(user, self.db_session)).
        menus = {
            "client": menu_client,
            "seller": menu_seller,
            "admin": menu_admin
        }
        menu_function = menus.get(user.role)
        if menu_function:
            # IMPORTANT: These are console-based functions.
            # They will still prompt for input in the console.
            # You'll need to replace these with actual GUI windows/dialogs later.
            try:
                # Pass the persistent session to the console-based menu function
                menu_function(user, self.db_session)
            except Exception as e: # Catch any exceptions from the console menu, including LogoutException
                print(f"Wystąpił błąd w menu użytkownika: {e}")
                self._handle_logout_request() # Force logout on error
        else:
            print(f"❌ Nieznana rola użytkownika: {user.role}")
            self._handle_logout_request() # Force logout for unknown role

    def _handle_logout_request(self):
        """
        Handles the logout request. Closes the persistent database session
        and resets the application state to logged-out.
        """
        print("\n🔒 Wylogowano. Zamykam sesję bazy danych.")
        # Do NOT close the session here if it's meant to be persistent for the app lifecycle
        # Instead, just clear current_user. The session will be closed on app exit.
        self.current_user = None
        self.loggedOut.emit() # Emit signal to show the start window again

    # Example of how you might expose a logout method to other GUI elements
    # (e.g., a "Logout" button in the main menu)
    def logout(self):
        self._handle_logout_request()

    def _close_db_session_on_exit(self):
        """
        Ensures the database session is closed when the application is about to quit.
        """
        if self.db_session:
            self.db_session.close()
            print("✅ Sesja bazy danych zamknięta podczas zamykania aplikacji.")
        self.db_session = None
