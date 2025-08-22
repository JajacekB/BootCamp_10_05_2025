import sys
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox, QGridLayout,
    QHBoxLayout ,QVBoxLayout, QApplication, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, Signal
import bcrypt
import pycountry
from sqlalchemy.exc import IntegrityError
from models.user import User
from validation.validation import is_valid_phone, is_valid_email
from database.base import SessionLocal
from repositories.read_methods import get_user_by
from repositories.write_methods import update_user


class UpdateUserWidget(QWidget):
    def __init__(self, session = None, user = None, controller = None):
        super().__init__()

        self.session = session or SessionLocal()
        self.user = user
        if not self.user:
            user_id = 16
            self.user = get_user_by(self.session, user_id = user_id)
        self.controller = controller
        self.user_data_dict = {}



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
        self.populate_user_data(user)

        # QTimer.singleShot(0, self._build_ui)

    def _build_ui(self):

        self.main_layout = QVBoxLayout()

        self.header_label =QLabel(">>> PRZEGLĄD PROFILU <<<")
        self.main_layout.addWidget(self.header_label)

        self.label_keys = QLabel()
        self.label_values = QLabel()
        self.label_keys.setFixedWidth(200)
        self.label_keys.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.label_values.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout_1 = QHBoxLayout()
        layout_1.addWidget(self.label_keys)
        layout_1.addWidget(self.label_values)
        layout_1.addStretch()

        self.update_profile_button = QPushButton("Edytuj profil")
        self.update_profile_button.setFixedWidth(200)
        self.update_profile_button.setFixedHeight(30)
        self.update_profile_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.update_profile_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.update_profile_button.clicked.connect(self.on_update_profile)

        self.change_password_button = QPushButton("Zmień hasło")
        self.change_password_button.setFixedWidth(250)
        self.change_password_button.setFixedHeight(30)
        self.change_password_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.change_password_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.change_password_button.clicked.connect(self.on_change_password)

        layout_2 = QHBoxLayout()
        layout_2.addWidget(self.update_profile_button)
        layout_2.addWidget(self.change_password_button)
        layout_2.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(layout_1)
        layout.addLayout(layout_2)

        self.container_1 = QWidget()
        self.container_1.setLayout(layout)
        self.main_layout.addWidget(self.container_1)

        update_user_grid = QGridLayout()

        self.title_label = QLabel("Twoje dane:", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        update_user_grid.addWidget(self.title_label, 0, 0, 1, 2)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText(self.user.first_name)
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText(self.user.last_name)
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText(self.user.login)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText(self.user.phone)
        self.phone_input.textChanged.connect(self._validate_phone_input)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(self.user.email)
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
        self.address_input.setPlaceholderText(self.user.address)
        self.address_layout.addRow("Podaj nowy adres:", self.address_input)
        update_user_grid.addLayout(self.address_layout, 3, 0, 1, 2)

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.setFixedSize(130, 30)
        self.cancel_button.setStyleSheet(
            "background-color: lightgreen;"
            " font-size: 18px; color: white;"
        )
        self.cancel_button.clicked.connect(self.on_click_clear_data)
        update_user_grid.addWidget(self.cancel_button, 4, 0, 1, 1)

        self.confirm_button = QPushButton("Zatwierdź")
        self.confirm_button.setFixedSize(130, 30)
        self.confirm_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.confirm_button.clicked.connect(self.handle_summary_data)
        update_user_grid.addWidget(self.confirm_button, 4, 1, 1, 1)

        self.summary_label = QLabel("")
        self.summary_label.setVisible(True)
        update_user_grid.addWidget(self.summary_label, 5, 0, 1, 1)

        self.save_data_button = QPushButton("Zapisz zmiany")
        self.save_data_button.setFixedSize(130, 30)
        self.save_data_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 18px; color: white;"
        )
        self.save_data_button.clicked.connect(self.on_click_update)
        self.save_data_button.hide()
        update_user_grid.addWidget(self.save_data_button, 5, 1, 1, 1)


        self.container_2 = QWidget()
        self.container_2.setLayout(update_user_grid)
        self.container_2.hide()
        self.main_layout.addWidget(self.container_2)





        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def populate_user_data(self, user):

        if not self.user:
            user_id = 16
            self.user = get_user_by(self.session, user_id = user_id)

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


    def on_update_profile(self):
        self.header_label.clear()
        self.header_label.setText(">>> EEDYCJA PROFILU <<<")
        self.container_1.hide()
        self.container_2.show()

    def handle_summary_data(self):

        def get_field_value(widget):

            text = widget.text().strip()
            return text if text else widget.placeholderText().strip()

        first_name = get_field_value(self.first_name_input)
        last_name = get_field_value(self.last_name_input)
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
            "email": email,
            "phone": phone,
            "address": address
        }

        summary_text = (
            f"Imię: {first_name}\n"
            f"Nazwisko: {last_name}\n"
            f"Email: {email}\n"
            f"Telefon: {phone}\n"
            f"Adres: {address}"
        )

        self.summary_label.setText(summary_text)
        self.summary_label.setStyleSheet("color: white;")

        self.confirm_button.hide()
        self.save_data_button.show()

        return self.summary_data

    def on_click_update(self):
        success, msg = update_user(self.session, self.user, self.summary_data)
        if success:
            self._reset_edit_mode()
            QMessageBox.information(self, "Sukces", "✅ Zaktualizowano pomyślnie!")
        else:
            QMessageBox.critical(self, "Błąd", f"❌ Wystąpił problem przy zapisie:\n{msg}")

    def on_click_clear_data(self):
        self._reset_edit_mode()


    def on_change_password(self):
        """

        :return:
        """

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

    def _reset_edit_mode(self):

        self.populate_user_data(self.user)
        self.container_2.hide()
        self.container_1.show()
        self.save_data_button.hide()
        self.confirm_button.show()
        self.summary_label.setText("")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UpdateUserWidget()
    main_window.show()
    sys.exit(app.exec())
