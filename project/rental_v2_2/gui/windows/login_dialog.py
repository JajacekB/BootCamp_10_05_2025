from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QFont, QPalette, QColor

# Import the backend authentication service
from services.auth_service import login_user_gui # We will create this new function

class LoginDialog(QDialog):
    # Define signals to communicate with the AppController
    # Emits the User object upon successful login
    login_successful = Signal(object)
    # Emitted when the user cancels the login process
    login_cancelled = Signal()

    def __init__(self, db_session, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Logowanie do MOTO VIBE 3000")
        self.db_session = db_session # Pass the database session to the dialog

        self.setFixedSize(400, 300) # Set a fixed size for the dialog

        # Set background to 18% gray, consistent with StartWindow
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2e2e2e"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # Title
        title_label = QLabel("Zaloguj się", self)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")
        main_layout.addWidget(title_label)

        # Message label for errors/feedback
        self.message_label = QLabel("", self)
        self.message_label.setFont(QFont("Arial", 12))
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: red;") # Default to red for errors
        main_layout.addWidget(self.message_label)

        # Login/Email Input
        login_layout = QHBoxLayout()
        login_label = QLabel("Login/Email:", self)
        login_label.setFont(QFont("Arial", 14))
        login_label.setStyleSheet("color: white;")
        self.login_input = QLineEdit(self)
        self.login_input.setPlaceholderText("Wprowadź login lub email")
        self.login_input.setFont(QFont("Arial", 14))
        self.login_input.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px;")
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_input)
        main_layout.addLayout(login_layout)

        # Password Input
        password_layout = QHBoxLayout()
        password_label = QLabel("Hasło:", self)
        password_label.setFont(QFont("Arial", 14))
        password_label.setStyleSheet("color: white;")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Wprowadź hasło")
        self.password_input.setFont(QFont("Arial", 14))
        self.password_input.setEchoMode(QLineEdit.Password) # Hide password characters
        self.password_input.setStyleSheet("background-color: #444; color: white; border-radius: 5px; padding: 5px;")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Zaloguj się", self)
        self.cancel_button = QPushButton("Anuluj", self)

        for btn in [self.login_button, self.cancel_button]:
            btn.setFont(QFont("Arial", 16))
            btn.setFixedHeight(40)
            btn.setStyleSheet(
                "background-color: #555;"
                "color: white;"
                "border-radius: 8px;"
                "padding: 5px 15px;"
            )
            btn.setCursor(Qt.PointingHandCursor) # Change cursor on hover

        self.login_button.clicked.connect(self._perform_login)
        self.cancel_button.clicked.connect(self._cancel_login)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        # Set focus to the login input initially
        self.login_input.setFocus()

    def _perform_login(self):
        """
        Attempts to log in the user using the provided credentials.
        """
        login_or_email = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login_or_email or not password:
            self.message_label.setText("Wprowadź login/email i hasło.")
            self.message_label.setStyleSheet("color: red;")
            return

        # Call the new GUI-friendly login function from auth_service
        user = login_user_gui(self.db_session, login_or_email, password)

        if user:
            self.message_label.setText(f"Zalogowano jako {user.first_name} {user.last_name} ({user.role}!")
            self.message_label.setStyleSheet("color: green;")
            # Emit the signal with the user object and close the dialog
            self.login_successful.emit(user)
            self.accept() # Close dialog with QDialog.Accepted result
        else:
            self.message_label.setText("Nieprawidłowy login/email lub hasło.")
            self.message_label.setStyleSheet("color: red;")
            # Clear password field for security
            self.password_input.clear()

    def _cancel_login(self):
        """
        Handles the cancel button click.
        """
        self.login_cancelled.emit()
        self.reject() # Close dialog with QDialog.Rejected result


