from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Signal, Qt


class RegisterWidget(QWidget):
    registration_finished = Signal(bool)  # True jeśli OK, False jeśli anulowano
    registration_cancelled = Signal()

    def __init__(self, session, parent=None, role=None, auto=False):
        super().__init__(parent)
        self.session = session
        self.auto = auto
        self.fixed_role = role  # Jeśli podana, pole roli jest zablokowane i ustawione na tę wartość

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Login
        self.login_label = QLabel("Login:")
        self.login_edit = QLineEdit()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_edit)

        # Hasło
        self.password_label = QLabel("Hasło:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)

        # Potwierdzenie hasła
        self.password_confirm_label = QLabel("Potwierdź hasło:")
        self.password_confirm_edit = QLineEdit()
        self.password_confirm_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_confirm_label)
        layout.addWidget(self.password_confirm_edit)

        # Rola (combo)
        self.role_label = QLabel("Rola:")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["client", "seller", "admin"])
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_combo)

        if self.fixed_role:
            self.role_combo.setCurrentText(self.fixed_role)
            self.role_combo.setDisabled(True)

        # Przyciski
        buttons_layout = QHBoxLayout()
        self.btn_register = QPushButton("Zarejestruj")
        self.btn_cancel = QPushButton("Anuluj")
        buttons_layout.addWidget(self.btn_register)
        buttons_layout.addWidget(self.btn_cancel)
        layout.addLayout(buttons_layout)

        # Podłączenie sygnałów
        self.btn_register.clicked.connect(self._on_register_clicked)
        self.btn_cancel.clicked.connect(self._on_cancel_clicked)

        if self.auto and self.fixed_role:
            # automatyczne uzupełnienie loginu i hasła
            self._auto_fill_credentials()

    def _auto_fill_credentials(self):
        # Przykład automatycznego wypełnienia pola login i hasło
        # Możesz zaimplementować wg własnej logiki
        suggested = f"{self.fixed_role.capitalize()}Auto"
        self.login_edit.setText(suggested)
        self.password_edit.setText(suggested)
        self.password_confirm_edit.setText(suggested)

    def _on_register_clicked(self):
        login = self.login_edit.text().strip()
        password = self.password_edit.text()
        password_confirm = self.password_confirm_edit.text()
        role = self.role_combo.currentText()

        if not login or not password:
            QMessageBox.warning(self, "Błąd", "Login i hasło są wymagane.")
            return

        if password != password_confirm:
            QMessageBox.warning(self, "Błąd", "Hasła nie są zgodne.")
            return

        # Tu dodaj walidacje, zapisy do bazy, itp.
        # Dla przykładu sygnalizujemy sukces:
        print(f"Rejestracja użytkownika: login={login}, rola={role}")

        # Emitujemy sygnał sukcesu
        self.registration_finished.emit(True)

    def _on_cancel_clicked(self):
        self.registration_cancelled.emit()