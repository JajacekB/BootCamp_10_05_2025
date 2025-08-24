import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox, QGroupBox, QHBoxLayout
    )
from PySide6.QtCore import Qt, QTimer, Signal
from sqlalchemy import desc
from datetime import date

from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
from models.rental_history import RentalHistory
from database.base import SessionLocal


class GetUsersWidget(QWidget):

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


        self.search_button = QPushButton("Pokaż")
        self.search_button.setStyleSheet(
            "background-color: green;"
            "font-size: 20px; color: white;"
            "border-radius: 8px; padding: 5px;"
        )
        self.search_button.setFixedSize(150, 35)
        self.search_button.clicked.connect(self.get_users_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addStretch()
        form_layout.addRow("", button_layout)

        filters_layout = QVBoxLayout()
        filters_layout.addLayout(form_layout)

        self.filters_group = QGroupBox("Filtr wyszukiwania")
        self.filters_group.setLayout(filters_layout)

        main_layout.addWidget(self.filters_group)

        self.list_widget = QListWidget()
        self.list_widget.setWordWrap(True)

        self.adjust_list_height()
        main_layout.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.show_user_details)

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

                if not vehicle_with_rent:
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

                if not vehicle_with_rent:
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
                self.adjust_list_height()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas pobierania danych:\n{e}")

    def show_user_details(self, item):
        # 1) Klik ignorujemy, jeśli to nie jest wiersz z listy użytkowników
        uid = item.data(Qt.UserRole)
        if not isinstance(uid, int):  # brak uid -> klik w "szczegóły", nic nie rób
            return

        try:
            vehicle_info = self.session.query(Vehicle).filter(Vehicle.borrower_id == uid).first()
            user_info = self.session.query(User).filter(User.id == uid).first()
            rent_info = self.session.query(RentalHistory).filter(
                RentalHistory.user_id == uid
            ).order_by(desc(RentalHistory.planned_return_date)).first()

            self.list_widget.blockSignals(True)
            self.list_widget.clear()

            if user_info:
                user_item = QListWidgetItem(f"Użytkownik: {user_info}")
            else:
                user_item = QListWidgetItem("Użytkownik: brak danych")
            user_item.setFlags(Qt.NoItemFlags)  # pasywny
            user_item.setData(Qt.UserRole, None)  # brak uid -> przyszłe kliki zignorujemy
            self.list_widget.addItem(user_item)

            if not rent_info:
                vehicle_item = QListWidgetItem("Nigdy nie wypożyczał żadnego pojazdu")
            else:
                start = rent_info.start_date
                planned = rent_info.planned_return_date
                start_str = start.strftime("%d.%m.%Y") if start else "brak daty startu"
                planned_str = planned.strftime("%d.%m.%Y") if planned else "brak daty zwrotu"

                if planned and planned < date.today():
                    vehicle_item = QListWidgetItem("Obecnie nie wypożycza żadnego pojazdu")
                else:
                    vehicle_text = []
                    vehicle_text.append(f"Pojazd: {vehicle_info}" if vehicle_info else "Pojazd: brak danych")
                    vehicle_text.append(f"Wynajęty od {start_str} do {planned_str}")
                    vehicle_item = QListWidgetItem("\n".join(vehicle_text))

            vehicle_item.setFlags(Qt.NoItemFlags)  # pasywny
            vehicle_item.setData(Qt.UserRole, None)  # brak uid -> przyszłe kliki zignorujemy

            # Gdy vehicle bedzie klikalny

            # vehicle_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            # vehicle_item.setData(Qt.UserRole, ("vehicle", id))

            self.list_widget.addItem(vehicle_item)

            self.adjust_list_height()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas pobierania danych:\n{e}")
        finally:
            self.list_widget.blockSignals(False)


    def adjust_list_height(self):
        count = self.list_widget.count()
        row_height = self.list_widget.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.list_widget.frameWidth()
        new_height = min(10, max(5, count)) * row_height + frame
        self.list_widget.setMinimumHeight(new_height)
        self.list_widget.setMaximumHeight(new_height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = GetUsersWidget()
    main_window.show()
    sys.exit(app.exec())