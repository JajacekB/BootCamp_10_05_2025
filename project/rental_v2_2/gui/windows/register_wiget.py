from PySide6.QtWidgets import (
    QWidget, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox, QGridLayout
)
from PySide6.QtCore import Qt, QTimer, Signal
import bcrypt
import pycountry
from sqlalchemy.exc import IntegrityError
from models.user import User
from validation.validation import is_valid_phone, is_valid_email


class RegisterWidget(QWidget):

    registration_cancelled = Signal()
    registration_finished = Signal(bool)

    def __init__(self, session, parent=None, role="client", auto=False):
        super().__init__(parent)
        self.session = session
        self.role = role
        self.auto = auto

        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e; /* Ciemne tło dla całego widgetu */
                color: #eee; /* Jasny kolor tekstu */
                font-size: 16px;
            }
            QPushButton {
                background-color: #555;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                font-size: 14px;
            }
        """)

        self.valid_style = "border: 1px solid #4CAF50;"
        self.invalid_style = "border: 1px solid #F44336;"

        self._build_ui()

    def _build_ui(self):


        self.main_layout = QGridLayout(self)

        self.title_label = QLabel("Podaj dane osobiste:", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(self.title_label, 0, 0, 1, 2)

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Numer telefonu")
        self.phone_input.textChanged.connect(self._validate_phone_input)
        self.email_input = QLineEdit()
        self.email_input.editingFinished.connect(self._validate_email_input)

        self.personal_data_layout = QFormLayout()
        self.personal_data_layout.addRow("Imię:", self.first_name_input)
        self.personal_data_layout.addRow("Nazwisko:", self.last_name_input)
        self.personal_data_layout.addRow("Telefon:", self.phone_input)
        self.personal_data_layout.addRow("Email:", self.email_input)
        self.main_layout.addLayout(self.personal_data_layout, 1, 0, 1, 2)

        self.address_label = QLabel("Podaj adres zamieszkania:", self)
        self.address_label.setAlignment(Qt.AlignCenter)
        self.address_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(self.address_label, 2, 0, 1, 2)

        self.street_input = QLineEdit()
        self.post_code_input = QLineEdit()
        self.city_input = QLineEdit()

        country_list = [country.name for country in pycountry.countries]
        country_list.sort()

        self.country_combo_box = QComboBox()
        self.country_combo_box.addItems(country_list)

        self.address_layout = QFormLayout()
        self.address_layout.addRow("Ulica i numer:", self.street_input)
        self.address_layout.addRow("Kod pocztowy:", self.post_code_input)
        self.address_layout.addRow("Miasto:", self.city_input)
        self.address_layout.addRow("Państwo:", self.country_combo_box)
        self.main_layout.addLayout(self.address_layout, 3, 0, 1, 2)

        self.login_label = QLabel("Podaj dane logowania:", self)
        self.login_label.setAlignment(Qt.AlignCenter)
        self.login_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(self.login_label, 4, 0, 1, 2)

        if self.auto and self.role == "seller":
            count = self.session.query(User).filter_by(role="seller").count()
            seller_number = str(count + 1).zfill(2)
            seller_login = f"Seller{seller_number}"
            raw_password = seller_login
            print(f"\nUtworzono login: {seller_login} | hasło: {raw_password}")

            self.login_input = QLineEdit(seller_login)
            self.login_input.setReadOnly(True)

            self.password_input = QLineEdit(raw_password)
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setReadOnly(True)

            login_layout = QFormLayout()
            login_layout.addRow("Login:", self.login_input)
            login_layout.addRow("Hasło:", self.password_input)
            self.main_layout.addLayout(login_layout, 5, 0, 1, 2)

        else:
            self.login_input = QLineEdit()
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setPlaceholderText("Musi zawierać 6 znaków, 1 wielką literę, 1 cyfrę")
            self.password_input.textChanged.connect(self._validate_password_input)

            self.confirm_password_input = QLineEdit()
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
            self.confirm_password_input.editingFinished.connect(self._validate_confirm_password)

            self.login_layout = QFormLayout()
            self.login_layout.addRow("Login:", self.login_input)
            self.login_layout.addRow("Hasło:", self.password_input)
            self.login_layout.addRow("Potwierdź hasło:", self.confirm_password_input)
            self.main_layout.addLayout(self.login_layout, 5, 0, 1, 2)

        self.cancel1_button = QPushButton("Anuluj")
        self.cancel1_button.setFixedSize(150, 45)
        self.cancel1_button.setStyleSheet(
            "background-color: red;"
            "font-size: 24px; color: white;"
            " border-radius: 8px; padding: 10px;"
        )
        self.cancel1_button.clicked.connect(self._cancel_registration)
        self.main_layout.addWidget(self.cancel1_button, 6, 0, 1, 1, alignment=Qt.AlignLeft)

        self.confirm_button = QPushButton("Zatwierdź")
        self.confirm_button.setFixedSize(150, 45)
        self.confirm_button.setStyleSheet(
            "background-color: green;"
            " font-size: 24px; color: white; color: white;"
            " border-radius: 8px; padding: 10px;"
        )
        self.confirm_button.clicked.connect(self._show_summary)
        self.main_layout.addWidget(self.confirm_button, 6, 1, 1, 1, alignment=Qt.AlignRight)

        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("color: white; font-size: 14px;")
        self.summary_label.setVisible(False)
        self.main_layout.addWidget(self.summary_label, 7, 0, 1, 2)

        self.cancel2_button = QPushButton("Anuluj")
        self.cancel2_button.setFixedSize(150, 45)
        self.cancel2_button.setStyleSheet(
            "background-color: #F44336; color: white; border-radius: 8px; padding: 10px;"
        )
        self.cancel2_button.setVisible(False)
        self.cancel2_button.clicked.connect(self._hide_summary)
        self.main_layout.addWidget(self.cancel2_button, 8, 0, 1, 1, alignment=Qt.AlignLeft)

        self.add_user_button = QPushButton("Dodaj użytkownika")
        self.add_user_button.setFixedSize(150, 45)
        self.add_user_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 8px; padding: 10px;"
        )
        self.add_user_button.setVisible(False)
        self.add_user_button.clicked.connect(self.register_client_gui)
        self.main_layout.addWidget(self.add_user_button, 8, 1, 1, 1, alignment=Qt.AlignRight)

        col_count = self.main_layout.columnCount()
        for col in range(col_count):
            self.main_layout.setColumnStretch(col, 1)

        last_row = self.main_layout.rowCount()
        self.main_layout.setRowStretch(last_row, 1)


    def _get_full_address(self):
        return (
            f"ul. {self.street_input.text()}, "
            f"{self.post_code_input.text()} "
            f"{self.city_input.text()}, "
            f"{self.country_combo_box.currentText()}"
        )


    def _validate_password_input(self, text):
        is_long_enough = len(text) >= 6
        has_upper_case = any(char.isupper() for char in text)
        has_digit = any(char.isdigit() for char in text)
        if is_long_enough and has_upper_case and has_digit:
            self.password_input.setStyleSheet(self.valid_style)
        else:
            self.password_input.setStyleSheet(self.invalid_style)


    def _validate_phone_input(self, text):
        if is_valid_phone(text):
            self.phone_input.setStyleSheet(self.valid_style)
        else:
            self.phone_input.setStyleSheet(self.invalid_style)


    def _validate_email_input(self):
        email = self.email_input.text()
        if is_valid_email(email):
            self.email_input.setStyleSheet(self.valid_style)
        else:
            self.email_input.setStyleSheet(self.invalid_style)


    def _validate_confirm_password(self):
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        if password == confirm_password and password:
            self.confirm_password_input.setStyleSheet(self.valid_style)
        else:
            self.confirm_password_input.setStyleSheet(self.invalid_style)


    def _cancel_registration(self):
        self.clear_form()
        self.registration_cancelled.emit()


    def _hide_summary(self):
        self.summary_label.setVisible(False)
        self.add_user_button.setVisible(False)
        self.cancel2_button.setVisible(False)
        self.confirm_button.setEnabled(True)


    def _show_summary(self):
        if not self._is_form_valid():
            print("\n❌ Formularz zawiera błędy. Popraw dane przed zatwierdzeniem.")
            return

        full_name = f"{self.first_name_input.text()} {self.last_name_input.text()}"
        address = self._get_full_address()
        login = self.login_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        summary_text = (
            f"Podsumowanie:\n\n"
            f"Imię i Nazwisko: {full_name}\n"
            f"Login: {login}\n"
            f"Telefon: {phone}\n"
            f"Email: {email}\n"
            f"Adres: {address}\n"
        )
        self.summary_label.setText(summary_text)

        self.summary_label.setVisible(True)
        self.add_user_button.setVisible(True)
        self.cancel2_button.setVisible(True)
        self.confirm_button.setEnabled(False)


    def _is_form_valid(self):
        password = self.password_input.text()

        phone_valid = is_valid_phone(self.phone_input.text())
        email_valid = is_valid_email(self.email_input.text())
        password_valid = (
            len(password) >= 6 and
            any(char.isupper() for char in password) and
            any(char.isdigit() for char in password)
        )
        confirm_password_valid = password == self.confirm_password_input.text()

        return phone_valid and email_valid and password_valid and confirm_password_valid


    def register_client_gui(self):
        if self._is_form_valid():
            first_name = self.first_name_input.text()
            last_name = self.last_name_input.text()
            login = self.login_input.text()
            phone = self.phone_input.text()
            email = self.email_input.text()

            password_hash = bcrypt.hashpw(self.password_input.text().encode('utf-8'), bcrypt.gensalt()).decode()
            full_address = self._get_full_address()

            try:
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    login=login,
                    phone=phone,
                    email=email,
                    password_hash=password_hash,
                    address=full_address,
                    role=self.role
                )
                self.session.add(new_user)
                self.session.commit()
                self.session.refresh(new_user)

                self.summary_label.setText("✅ Użytkownik został dodany pomyślnie.")
                self.summary_label.setStyleSheet("color: #4CAF50; font-size: 14px;")

                self.add_user_button.setEnabled(False)
                self.cancel2_button.setEnabled(False)

                # Emitujemy sygnał zakończenia rejestracji z True (sukces)
                self.registration_finished.emit(True)
                return new_user

            except IntegrityError:
                self.session.rollback()

                self.summary_label.setText("❌ Login, telefon lub email już istnieje.")
                self.summary_label.setStyleSheet("color: #F44336; font-size: 14px;")

                self.add_user_button.setEnabled(False)
                self.cancel2_button.setEnabled(False)

                # Emitujemy sygnał zakończenia rejestracji z False (błąd)
                self.registration_finished.emit(False)
                return None
        else:
            self.summary_label.setText("❌ Formularz zawiera błędy. Popraw dane i spróbuj ponownie.")
            self.summary_label.setStyleSheet("color: #F44336; font-size: 14px;")
            self.summary_label.setVisible(True)
            return None

    def clear_form(self):
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.phone_input.clear()
        self.phone_input.setStyleSheet("")
        self.email_input.clear()
        self.email_input.setStyleSheet("")
        self.street_input.clear()
        self.post_code_input.clear()
        self.city_input.clear()
        self.login_input.clear()
        self.password_input.clear()
        self.password_input.setStyleSheet("")
        if hasattr(self, 'confirm_password_input'):
            self.confirm_password_input.clear()
            self.confirm_password_input.setStyleSheet("")
        self.summary_label.setVisible(False)
        self.add_user_button.setVisible(False)
        self.cancel2_button.setVisible(False)
        self.confirm_button.setEnabled(True)