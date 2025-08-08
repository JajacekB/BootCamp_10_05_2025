import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox
    )
from PySide6.QtCore import Qt, QTimer, Signal
from sqlalchemy import desc
from datetime import date

from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
from models.rental_history import RentalHistory
# from models.repair_history import RepairHistory
# from models.invoice import Invoice
from database.base import SessionLocal


class GetUsers(QWidget):

    def __init__(self, session=None):
        super().__init__()
        self.session =  session or SessionLocal()

        self.setWindowTitle("Klienci")

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
        self._build_ui()

    def _build_ui(self):

        with SessionLocal() as session:

            users_optins = ["Wszyscy", "Z wypożyczeniem", "Bez wypożyczenia"]

            main_layout = QVBoxLayout()

            title_label = QLabel("Przegląd klientów wypozyczalni:")
            title_label.setStyleSheet("font-size: 28px; color: white; ")
            title_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(title_label)

            self.status_combo_box = QComboBox()
            self.status_combo_box.addItems(users_optins)

            form_layout = QFormLayout()
            form_layout.addRow("Kótych kientów chcesz przeglądać?", self.status_combo_box)
            main_layout.addLayout(form_layout)

            self.list_widget = QListWidget()
            main_layout.addWidget(self.list_widget)
            self.list_widget.itemClicked.connect(self.show_user_details)

            search_button = QPushButton("Pokaż")
            search_button.setStyleSheet("font-size: 24; color: white; border-radius: 8px; padding: 10px; ")
            search_button.setFixedSize(150, 45)
            search_button.clicked.connect(self.get_users_list)

            main_layout.addWidget(search_button, alignment=Qt.AlignRight)

            main_layout.addStretch()
            self.setLayout(main_layout)


    def get_users_list(self):

        self.list_widget.clear()
        users_type = self.status_combo_box.currentText()

        try:
            if users_type == "Z wypożyczeniem":
                vehicle_with_rent = self.session.query(Vehicle).filter(
                    Vehicle.is_available == False
                ).all()

                if not users_type:
                    QMessageBox.information(self, "Informacja", "Obecnie żaden klient nie wypożycza pojazdów.")
                    return

                user_ids = [u.borrower_id for u in vehicle_with_rent]

                users = self.session.query(User).filter(
                    User.id.in_(user_ids),
                    User.role == "client"
                ).all()

            elif users_type == "Bez wypożyczenia":
                vehicle_with_rent = self.session.query(Vehicle).filter(
                    Vehicle.is_available == False
                ).all()

                if not users_type:
                    QMessageBox.information(self, "Informacja", "Brak klientów bez wypożyczenia.")
                    return

                user_ids = [u.borrower_id for u in vehicle_with_rent]

                users = self.session.query(User).filter(
                    User.id.notin_(user_ids),
                    User.role == "client"
                ).all()

            else:
                users = self.session.query(User).filter(User.role == "client").all()

                if not users:
                    QMessageBox.information(self, "Informacja", "Żaden klient nie jest zarejestrowany w wypożyczalni.")
                    return

            user_view = defaultdict(list)
            for u in (users):
                key = (u.id, u.first_name, u.last_name, u.login)
                user_view[key].append(u)

            for (uid, first_name, last_name, login) in user_view:
                user_strs = f"ID: [{uid:03d}]  -  {first_name} {last_name},  login: {login}."
                item = QListWidgetItem(user_strs)
                item.setData(Qt.UserRole, uid)
                self.list_widget.addItem(item)

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas pobierania danych:\n{e}")


    def show_user_details(self, item):

        uid = item.data(Qt.UserRole)

        try:
            vehicle_info = self.session.query(Vehicle).filter(Vehicle.borrower_id == uid).first()
            user_info = self.session.query(User).filter(User.id == uid).first()
            rent_info = self.session.query(RentalHistory).filter(
                RentalHistory.user_id == int(uid)).order_by(
                desc(RentalHistory.planned_return_date)
            ).first()

            if not rent_info:
                user_details = f"Uzytkownik: {user_info}\nNigdy nie wypożyczał żadnego pojazdy"

            else:
                start = rent_info.start_date
                planned = rent_info.planned_return_date
                start_str = start.strftime("%d.%m.%Y") # if start else "brak daty startu"
                planned_str = planned.strftime("%d.%m.%Y") # if planned else "brak daty zwrotu"

                if planned < date.today():
                    user_details = f"Użytkownik: {user_info}\nObecnie nie wypozycza, żadnego ppojazdu."

                else:

                    user_details = (f"{user_info}\n"
                                    f"{vehicle_info}\n"
                                    f"Wynajęty od {start_str} do {planned_str}")

            self.list_widget.clear()
            item_1 = QListWidgetItem(user_details)
            item_1.setFlags(Qt.ItemIsEnabled)
            self.list_widget.addItem(item_1)

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas pobierania danych:\n{e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = GetUsers()
    main_window.show()
    sys.exit(app.exec())