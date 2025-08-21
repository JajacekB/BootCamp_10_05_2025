import sys
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox, QGridLayout,
    QHBoxLayout ,QVBoxLayout, QApplication
)
from PySide6.QtCore import Qt, QTimer, Signal
import bcrypt
import pycountry
from sqlalchemy.exc import IntegrityError
from models.user import User
from validation.validation import is_valid_phone, is_valid_email
from database.base import SessionLocal
from repositories.get_methods import get_user_by


class UpdateUserWidget(QWidget):
    def __init__(self, session = None, user = None, controller = None):
        super().__init__()

        self.session = session or SessionLocal()
        self.user = user
        self.controller = controller
        self.user_data_dict = {}

        self._build_ui()

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

        QTimer.singleShot(0, self._build_ui)

    def _build_ui(self):

        self.main_layout = QVBoxLayout()

        self.title_label =QLabel(">>> PRZEGLĄD PROFILU <<<")
        self.main_layout.addWidget(self.title_label)


        self.user = self.handle_user_data()
        if not self.user:
            self.main_layout.addWidget(QLabel("Brak danych użytkownika"))
        else:
            self.main_layout.addWidget(self.user_display_widget())





        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def user_display_widget(self):
        excluded = {"id", "password_hash", "registration_day", "is_active"}
        user = self.handle_user_data()
        if not user:
            return None  # brak danych

        # słownik kolumna:wartość z obiektu User
        user_dict = {
            c.name: getattr(user, c.name)
            for c in user.__table__.columns
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

        keys_str = "\n".join(display_dict.keys())
        values_str = "\n".join(str(v) for v in display_dict.values())

        # stworzenie widgetu z układem
        label_keys = QLabel(keys_str)
        label_keys.setMaximumWidth(200)
        label_values = QLabel(values_str)
        layout = QHBoxLayout()
        layout.addWidget(label_keys)
        layout.addWidget(label_values)

        container = QWidget()
        container.setLayout(layout)
        return container

    def handle_user_data(self):
        if not self.user:
            user_id = 16
            self.user = get_user_by(self.session, user_id = user_id)
        return self.user



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UpdateUserWidget()
    main_window.show()
    sys.exit(app.exec())
