import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox
    )
from PySide6.QtCore import Qt, QTimer, Signal

from services.vehicle_avability import get_unavailable_vehicle, get_available_vehicles
from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
from database.base import SessionLocal



class GetVehicleWidget(QWidget):

    registration_cancelled = Signal()
    registration_finished = Signal(bool)

    def __init__(self, session=None, parent=None, role = "admin", auto = False):
        super().__init__()
        self.session =  session or SessionLocal()
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

        self.main_layout = QVBoxLayout()

        self.title_label = QLabel("Przegląd pojazdów w wypozyczalni:" )
        self.title_label.setStyleSheet("font-size: 28px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.status_combo_box = QComboBox()
        self.status_combo_box.addItems(["Wszystkie", "Dostępne", "Niedostępne"])

        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(["Wszystkie", "Samochody", "Skutery", "Rowery"])

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Wybierz czy chcez przeglądać pojazdy dostępne", self.status_combo_box)
        self.form_layout.addRow("Jaki rodzaj pojazdów chcesz przeglądać:", self.type_combo_box)

        self.main_layout.addLayout(self.form_layout)

        self.list_widget = QListWidget()

        self.main_layout.addWidget(self.list_widget)

        self.search_button = QPushButton("Pokaż")
        self.search_button.setStyleSheet(
            "background-color: green;"
            " font-size: 24px; color: white;"
            " border-radius: 8px; padding: 10px; ")
        self.search_button.setFixedSize(150, 45)
        self.search_button.clicked.connect(self.get_vehicles_list)

        self.main_layout.addWidget(self.search_button, alignment=Qt.AlignRight)

        self.list_widget.itemClicked.connect(self.handle_item_clicked)

        self.main_layout.addStretch()

        self.setLayout(self.main_layout)



    def get_vehicles_list(self):
        self.list_widget.clear()

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
            available_vehicles = get_available_vehicles(self.session, vehicle_type=vehicle_type)

        elif available_is == "Niedostępne":
            available_vehicles, _ = get_unavailable_vehicle(self.session, vehicle_type=vehicle_type)

        else:
            if vehicle_type == "all":
                available_vehicles = self.session.query(Vehicle).all()

            else:
                available_vehicles = self.session.query(Vehicle).filter(Vehicle.type == vehicle_type).all()

        if not available_vehicles:
            print("\n🚫 Brak pasujących pojazdów.")
            return

        vehicles_sorted = sorted(
            available_vehicles,
            key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model, v.individual_id)
        )
        vehicles = defaultdict(list)
        for v in (vehicles_sorted):
            key = (v.brand, v.vehicle_model, v.cash_per_day)
            vehicles[key].append(v)

        for (brand, model, cash_per_day), group in vehicles.items():
            count = len(group)
            display_text = f"{brand} {model}  –  {cash_per_day:.2f} zł/dzień - ({count} szt.)"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, group)  # Przechowujemy całą grupę pojazdów
            self.list_widget.addItem(item)

    def show_group_members(self, group):
        self.list_widget.clear()

        for v in group:
            display_text = (
                f"🔹 {v.brand} {v.vehicle_model}  -  "
                f"{v.cash_per_day:.2f} zł/dzień,  [{v.individual_id}]"
            )
            item = QListWidgetItem(display_text)
            item.setFlags(Qt.ItemIsEnabled)  # nie można ich zaznaczać/klikać
            self.list_widget.addItem(item)

        # przycisk powrotu
        return_item = QListWidgetItem("↩ Wróć do listy grup")
        return_item.setData(Qt.UserRole, "return")
        self.list_widget.addItem(return_item)


    def handle_item_clicked(self, item):
        data = item.data(Qt.UserRole)

        if data == "return":
            self.get_vehicles_list()  # wróć do widoku grup
            return

        if isinstance(data, list):
            self.show_group_members(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = GetVehicleWidget()
    main_window.show()
    sys.exit(app.exec())
