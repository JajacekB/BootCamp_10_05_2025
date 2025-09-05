import bcrypt
from PySide6.QtWidgets import (QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, Signal

from validation.validation import is_valid_phone, is_valid_email


class UpdateUserView(QWidget):

    handle_update_password_data = Signal(dict)
    handle_update_user_data = Signal(dict)

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("Przegląd profilu")

        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e; /* Ciemne tło dla całego widgetu */
                color: #eee; /* Jasny kolor tekstu */
                font-size: 18px;
            }
            QPushButton {
                background-color: #555;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                font-size: 16px;
            }
        """)

        self.valid_style = "border: 1px solid #4CAF50;"
        self.invalid_style = "border: 1px solid #F44336;"
        self.regular_style = ""

        self._build_ui()
        self.populate_user_data()

    def _build_ui(self):

        main_layout = QVBoxLayout()

        self.header_label = QLabel(">>> PRZEGLĄD PROFILU <<<")
        self.header_label.setStyleSheet("font-size: 24px; color: #A9C1D9; ")
        main_layout.addWidget(self.header_label)

        self.label_keys = QLabel()
        self.label_values = QLabel()
        self.label_keys.setMinimumWidth(200)
        self.label_keys.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.label_values.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout_1 = QHBoxLayout()
        layout_1.addWidget(self.label_keys)
        layout_1.addWidget(self.label_values)
        layout_1.addStretch()

        self.update_profile_button = QPushButton("Edytuj profil")
        self.update_profile_button.setMinimumWidth(200)
        self.update_profile_button.setFixedHeight(30)
        self.update_profile_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.update_profile_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.update_profile_button.clicked.connect(self._on_update_profile)

        self.change_password_button = QPushButton("Zmień hasło")
        self.change_password_button.setMinimumWidth(250)
        self.change_password_button.setFixedHeight(30)
        self.change_password_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.change_password_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.change_password_button.clicked.connect(self._on_change_password)

        layout_2 = QHBoxLayout()
        layout_2.addWidget(self.update_profile_button)
        layout_2.addWidget(self.change_password_button)
        layout_2.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(layout_1)
        layout.addLayout(layout_2)


        self.container_1 = QWidget()
        self.container_1.setLayout(layout)
        main_layout.addWidget(self.container_1)

        update_user_grid = QGridLayout()

        self.title_label = QLabel("Twoje dane:", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        update_user_grid.addWidget(self.title_label, 0, 0, 1, 2)

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.login_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText(self.user.phone)
        self.email_input = QLineEdit()
        self.email_input.editingFinished.connect(self._validate_email_input)

        self.personal_data_layout = QFormLayout()
        self.personal_data_layout.addRow("Imię:", self.first_name_input)
        self.personal_data_layout.addRow("Nazwisko:", self.last_name_input)
        self.personal_data_layout.addRow("Login:", self.login_input)
        self.personal_data_layout.addRow("Telefon:", self.phone_input)
        self.personal_data_layout.addRow("Email:", self.email_input)
        update_user_grid.addLayout(self.personal_data_layout, 1, 0, 1, 2)

        self.address_label = QLabel(f"Adres zamieszkania:\n {self.user.address}", self)
        self.address_label.setAlignment(Qt.AlignCenter)
        self.address_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        update_user_grid.addWidget(self.address_label, 2, 0, 1, 2)

        self.address_input = QLineEdit()
        self.address_layout = QFormLayout()
        self.address_layout.addRow("Podaj nowy adres:", self.address_input)
        update_user_grid.addLayout(self.address_layout, 3, 0, 1, 2)

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.setMinimumSize(200, 30)
        self.cancel_button.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 18px; color: white;"
        )
        self.cancel_button.clicked.connect(self._on_click_clear_data)
        update_user_grid.addWidget(self.cancel_button, 4, 0, 1, 1)

        self.confirm_button = QPushButton("Zatwierdź")
        self.confirm_button.setMinimumSize(200, 30)
        self.confirm_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.confirm_button.clicked.connect(self._handle_summary_data)
        update_user_grid.addWidget(self.confirm_button, 4, 1, 1, 1)

        self.summary_label = QLabel("")
        self.summary_label.setVisible(True)
        update_user_grid.addWidget(self.summary_label, 5, 0, 1, 1)

        self.save_data_button = QPushButton("Zapisz zmiany")
        self.save_data_button.setMinimumSize(200, 30)
        self.save_data_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.save_data_button.clicked.connect(self._on_click_update)
        self.save_data_button.hide()
        update_user_grid.addWidget(self.save_data_button, 5, 1, 1, 1)

        self.container_2 = QWidget()
        self.container_2.setLayout(update_user_grid)
        self.container_2.hide()
        main_layout.addWidget(self.container_2, alignment=Qt.AlignLeft)

        password_grid = QGridLayout()
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)

        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("Musi zawierać 6 znaków, 1 wielką literę, 1 cyfrę")
        self.new_password_input.textChanged.connect(self._validate_password_input)

        self.confirm_new_password_input = QLineEdit()
        self.confirm_new_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_new_password_input.editingFinished.connect(self._validate_confirm_password)

        self.login_layout = QFormLayout()
        self.login_layout.addRow("Podaj stare hasło:", self.old_password_input)

        self.container_login = QWidget()
        self.container_login.setLayout(self.login_layout)
        self.container_login.hide()
        password_grid.addWidget(self.container_login, 0, 0, 1, 2)

        self.cancel_1_button = QPushButton("Anuluj")
        self.cancel_1_button.setMinimumSize(200, 30)
        self.cancel_1_button.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 18px; color: white;"
        )
        self.cancel_1_button.clicked.connect(self._on_click_clear_data)
        password_grid.addWidget(self.cancel_1_button, 1, 0, 1, 1)

        self.confirm_1_button = QPushButton("Potwierdź hasło")
        self.confirm_1_button.setMinimumSize(200, 30)
        self.confirm_1_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.confirm_1_button.clicked.connect(self._on_click_old_password)
        password_grid.addWidget(self.confirm_1_button, 1, 1, 1, 1)

        self.password_confirm_layout = QFormLayout()
        self.password_confirm_layout.addRow("Podaj nowe hasło:", self.new_password_input)
        self.password_confirm_layout.addRow("Potwierdź nowe hasło:", self.confirm_new_password_input)

        self.container_password = QWidget()
        self.container_password.setLayout(self.password_confirm_layout)
        self.container_password.hide()
        password_grid.addWidget(self.container_password, 2, 0, 1, 2)

        self.cancel_2_button = QPushButton("Anuluj")
        self.cancel_2_button.setMinimumSize(200, 30)
        self.cancel_2_button.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 18px; color: white;"
        )
        self.cancel_2_button.clicked.connect(self._on_click_clear_data)
        password_grid.addWidget(self.cancel_2_button, 3, 0, 1, 1)

        self.confirm_2_button = QPushButton("Zmień")
        self.confirm_2_button.setMinimumSize(200, 30)
        self.confirm_2_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.confirm_2_button.clicked.connect(self._handle_update_password)
        password_grid.addWidget(self.confirm_2_button, 3, 1, 1, 1)

        self.container_3 = QWidget()
        self.container_3.setLayout(password_grid)
        self.container_3.hide()

        main_layout.addWidget(self.container_3, alignment=Qt.AlignLeft)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def populate_user_data(self):
        # self.user = get_user_by(self.session, user_id=user.id)

        excluded = {"id", "password_hash", "registration_day", "is_active"}
        user_dict = {
            c.name: getattr(self.user, c.name)
            for c in self.user.__table__.columns
            if c.name not in excluded
        }

        labels_map = {
            "id": "ID:",
            "login": "Login:",
            "email": "E-mail:",
            "first_name": "Imię:",
            "last_name": "Nazwisko:",
            "address": "Adres zamieszkania:",
            "phone": "Telefon:"
        }

        display_dict = {labels_map[k]: v for k, v in user_dict.items() if k in labels_map}

        self.keys_str = "\n".join(display_dict.keys())
        self.values_str = "\n".join(str(v) for v in display_dict.values())

        self.label_keys.setText(self.keys_str)
        self.label_values.setText(self.values_str)

    def _on_update_profile(self):

        self.first_name_input.setPlaceholderText(self.user.first_name)
        self.last_name_input.setPlaceholderText(self.user.last_name)
        self.login_input.setPlaceholderText(self.user.login)
        self.phone_input.setPlaceholderText(self.user.phone)
        self.email_input.setPlaceholderText(self.user.email)
        self.address_input.setPlaceholderText(self.user.address)

        self.header_label.clear()
        self.header_label.setText(">>> EDYCJA PROFILU <<<")
        self.container_1.hide()
        self.container_2.show()

    def _handle_summary_data(self):

        def get_field_value(widget):

            text = widget.text().strip()
            return text if text else widget.placeholderText().strip()

        first_name = get_field_value(self.first_name_input)
        last_name = get_field_value(self.last_name_input)
        login = get_field_value(self.login_input)
        email = get_field_value(self.email_input)
        phone = get_field_value(self.phone_input)
        address = get_field_value(self.address_input)

        phone_valid = is_valid_phone(phone)
        email_valid = is_valid_email(email)

        if not phone_valid or not email_valid:
            self.summary_label.setText(
                "❌ Formularz zawiera błędy!\n"
                f"{'Błędny numer telefonu.\n' if not phone_valid else ''}"
                f"{'Błędny email.' if not email_valid else ''}"
            )
            self.summary_label.setStyleSheet("color: red;")
            return  None

        self.summary_data = {
            "first_name": first_name,
            "last_name": last_name,
            "login": login,
            "email": email,
            "phone": phone,
            "address": address
        }

        summary_text = (
            f"Imię: {first_name}\n"
            f"Nazwisko: {last_name}\n"
            f"Login: {login}\n"
            f"Email: {email}\n"
            f"Telefon: {phone}\n"
            f"Adres: {address}"
        )

        self.summary_label.setText(summary_text)
        self.summary_label.setStyleSheet("color: white;")

        self.confirm_button.hide()
        self.save_data_button.show()

        return self.summary_data

    def _on_click_update(self):
        self.handle_update_user_data.emit(self.summary_data)

    def update_user_data_confirmation(self, success, msg, user):

        if success:
            self._reset_edit_mode()
            self.header_label.setText(">>> PRZEGLĄD PROFILU <<<")
            self.user = user
            QMessageBox.information(self, "Sukces", "✅ Zaktualizowano pomyślnie!")
        else:
            QMessageBox.critical(self, "Błąd", f"❌ Wystąpił problem przy zapisie:\n{msg}")


    def _on_change_password(self):
        self.header_label.setText(">>> ZMIANA HASŁA <<<")
        self.container_1.hide()
        self.container_2.hide()
        self.container_3.show()
        self.cancel_1_button.show()
        self.confirm_1_button.show()
        self.cancel_2_button.hide()
        self.confirm_2_button.hide()
        self.container_login.show()

    def _on_click_old_password(self):
        password = self.old_password_input.text().strip()
        if not bcrypt.checkpw(password.encode("utf-8"), self.user.password_hash.encode("utf-8")):
            QMessageBox.critical(self, "Błąd", f"❌ błędne hasło.")
            self.old_password_input.clear()
            return

        self.container_login.hide()
        self.cancel_1_button.hide()
        self.confirm_1_button.hide()
        self.container_password.show()
        self.cancel_2_button.show()
        self.confirm_2_button.show()

    def _handle_update_password(self):
        new_password = self.new_password_input.text().strip()
        confirm_new_password = self.confirm_new_password_input.text().strip()
        if not new_password == confirm_new_password:
            QMessageBox.critical(self, "Błąd", f"❌ Hasła nie są jednakowe.")
            self.confirm_new_password_input.clear()
            return

        new_password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.summary_data = {
            "password_hash": new_password_hash
        }
        self.handle_update_password_data.emit(self.summary_data)

    def update_password_confirm(self, success, msg):

        if success:
            self.header_label.setText(">>> PRZEGLĄD PROFILU <<<")
            self.new_password_input.setStyleSheet(self.regular_style)
            self.new_password_input.clear()
            self.confirm_new_password_input.setStyleSheet(self.regular_style)
            self.confirm_new_password_input.clear()
            self._reset_edit_mode()
            QMessageBox.information(self, "Sukces", "✅ Zaktualizowano pomyślnie!")
        else:
            QMessageBox.critical(self, "Błąd", f"❌ Wystąpił problem przy zapisie:\n{msg}")

    def _on_click_clear_data(self):
        self._reset_edit_mode()

    def _reset_edit_mode(self):

        self.populate_user_data()
        self.header_label.setText(">>> PRZEGLĄD PROFILU <<<")
        self.container_3.hide()
        self.container_2.hide()
        self.container_1.show()
        self.save_data_button.hide()
        self.confirm_button.show()
        self.cancel_1_button.hide()
        self.confirm_1_button.hide()
        self.cancel_2_button.hide()
        self.confirm_2_button.hide()
        self.container_password.hide()
        self.old_password_input.clear()

        inputs = [
            self.first_name_input,
            self.last_name_input,
            self.login_input,
            self.phone_input,
            self.email_input,
            self.old_password_input,
            self.new_password_input,
            self.confirm_new_password_input,
        ]
        for widget in inputs:
            widget.clear()
            widget.setStyleSheet(self.regular_style)

        self.summary_label.setText("")

    def _validate_phone_input(self, text):
        print("Sprawdzam numer_1:", text, "=>", is_valid_phone(text))
        if is_valid_phone(text):
            self.phone_input.setStyleSheet(self.valid_style)
            print("Sprawdzam numer_2:", text, "=>", is_valid_phone(text))
        else:
            self.phone_input.setStyleSheet(self.invalid_style)
            print("Sprawdzam numer_3:", text, "=>", is_valid_phone(text))

    def _validate_email_input(self):
        email = self.email_input.text()
        if is_valid_email(email):
            self.email_input.setStyleSheet(self.valid_style)
        else:
            self.email_input.setStyleSheet(self.invalid_style)

    def _validate_password_input(self, text):
        is_long_enough = len(text) >= 6
        has_upper_case = any(char.isupper() for char in text)
        has_digit = any(char.isdigit() for char in text)
        if is_long_enough and has_upper_case and has_digit:
            self.new_password_input.setStyleSheet(self.valid_style)
        else:
            self.new_password_input.setStyleSheet(self.invalid_style)

    def _validate_confirm_password(self):
        password = self.new_password_input.text()
        confirm_password = self.confirm_new_password_input.text()
        if password == confirm_password and password:
            self.confirm_new_password_input.setStyleSheet(self.valid_style)
        else:
            self.confirm_new_password_input.setStyleSheet(self.invalid_style)