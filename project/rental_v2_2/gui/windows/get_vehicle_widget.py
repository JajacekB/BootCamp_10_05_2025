import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem
    )
from PySide6.QtCore import Qt, QTimer, Signal

from services.vehicle_avability import get_unavailable_vehicle, get_available_vehicles
from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
# from models.rental_history import RentalHistory
# from models.repair_history import RepairHistory
# from models.invoice import Invoice
from database.base import SessionLocal



class GetVehicleWidget(QWidget):

    registration_cancelled = Signal()
    registration_finished = Signal(bool)

    def __init__(self, session=None, parent=None, role = "admin", auto = False):
        super().__init__()
        self.session = session
        self.role = role
        self.auto = auto
        self.setWindowTitle("Pojazdy")

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

        status_options = ["Wszystkie", "Dostępne", "Niedostępne"]
        vehicle_type_options = ["Wszystkie", "Samochody", "Skutery", "Rowery"]

        main_layout = QVBoxLayout()

        title_label = QLabel("Przegląd pojazdów w wypozyczalni:" )
        title_label.setStyleSheet("font-size: 28; color: white; ")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.status_combo_box = QComboBox()
        self.status_combo_box.addItems(status_options)

        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(vehicle_type_options)

        form_layout = QFormLayout()
        form_layout.addRow("Wybierz czy chcez przeglądać pojazdy dostępne", self.status_combo_box)
        form_layout.addRow("Jaki rodzaj pojazdów chcesz przeglądać:", self.type_combo_box)

        main_layout.addLayout(form_layout)

        self.list_widget = QListWidget()
        # list_vehicles = get_list()
        # for vehicle in list_vehicles:
        #     item = QListWidgetItem(str(vehicle))
        #     item.setData(Qt.UserRole, vehicle)
        #     list_widget.addItem(item)

        main_layout.addWidget(self.list_widget)

        search_button = QPushButton("Pokaż")
        search_button.setStyleSheet("font-size: 24; color: white; border-radius: 8px; padding: 10px; ")
        search_button.setFixedSize(150, 45)
        search_button.clicked.connect(self.get_list)


        main_layout.addWidget(search_button, alignment=Qt.AlignRight)







        main_layout.addStretch()

        self.setLayout(main_layout)



    def get_list(self):
        self.list_widget.clear()

        with SessionLocal() as session:
            vehicle_type_input = self.type_combo_box.currentText()
            available_is = self.status_combo_box.currentText()

            vehicle_type_options = {
                "Wszystkie": "all",
                "Samochody": "car",
                "Skutery": "scooter",
                "Rowery": "bike"
            }
            vehicle_type = vehicle_type_options.get(vehicle_type_input, "all")

            if available_is == "Dostępne":
                available_vehicles = get_available_vehicles(session, vehicle_type=vehicle_type)


            elif available_is == "Niedostępne":
                available_vehicles, _ = get_unavailable_vehicle(session, vehicle_type=vehicle_type)


            else:
                if vehicle_type == "all":
                    available_vehicles = session.query(Vehicle).all()

                else:
                    available_vehicles = session.query(Vehicle).filter(Vehicle.type == vehicle_type).all()

            if not available_vehicles:
                print("\n🚫 Brak pasujących pojazdów.")
                return

            vehicles_sorted = sorted(
                available_vehicles,
                key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model)
            )
            vehicles = defaultdict(list)
            for v in (vehicles_sorted):
                key = (v.brand, v.vehicle_model, v.cash_per_day)
                vehicles[key].append(v)

            for (brand, model, cash_per_day), group in vehicles.items():
                count = len(group)
                display_text = f"{brand} {model} – {cash_per_day:.2f} zł/dzień - ({count} szt.)"
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, group)  # Przechowujemy całą grupę pojazdów
                self.list_widget.addItem(item)




# def get_list():
#     with SessionLocal() as session:
#         vehicle_list = session.query(Vehicle).all()
#         # wymusz dostęp do wszystkich pól, żeby SQLAlchemy załadowało dane zanim sesja się zamknie
#         for v in vehicle_list:
#             _ = v.vehicle_id
#             _ = v.brand
#             _ = v.vehicle_model
#             _ = v.cash_per_day
#             _ = v.is_available
#             _ = v.return_date
#             _ = v.individual_id
#             # polimorfizm: jeśli to Car, Scooter lub Bike, wymusz dostęp do specyficznych atrybutów:
#             if isinstance(v, Car):
#                 _ = v.size
#                 _ = v.fuel_type
#             elif isinstance(v, Scooter):
#                 _ = v.max_speed
#             elif isinstance(v, Bike):
#                 _ = v.bike_type
#                 _ = v.is_electric
#         return vehicle_list







if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = GetVehicleWidget()
    main_window.show()
    sys.exit(app.exec())


# def on_search_clicked(self):
#     status = self.status_combo_box.currentText()
#     vehicle_type = self.type_combo_box.currentText()
#     filtered_vehicles = get_vehicles_filtered(self.session, status, vehicle_type)
#     self.list_widget.clear()
#     for v in filtered_vehicles:
#         item = QListWidgetItem(str(v))
#         item.setData(Qt.UserRole, v)
#         self.list_widget.addItem(item)