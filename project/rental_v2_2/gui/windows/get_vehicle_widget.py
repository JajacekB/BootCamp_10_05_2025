import platform
import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox,
        QApplication, QListWidget, QListWidgetItem, QMessageBox
    )
from PySide6.QtCore import Qt, QTimer, Signal

from services.vehicle_avability import get_unavailable_vehicle, get_available_vehicles
from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
from database.base import SessionLocal



class GetVehicleWidget(QWidget):

    list_updated = Signal()
    registration_cancelled = Signal()
    vehicle_selected = Signal(object)
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

        self.vehicle_list = QListWidget()
        font = self.vehicle_list.font()
        system = platform.system()

        if system == "Windows":
            font.setFamily("Consolas")
        elif system == "Darwin":  # macOS
            font.setFamily("Menlo")
        else:  # Linux i inne
            font.setFamily("DejaVu Sans Mono")

        self.vehicle_list.setFont(font)
        self.adjust_list_height()
        self.vehicle_list.itemClicked.connect(self.handle_item_clicked)
        self.main_layout.addWidget(self.vehicle_list)


        self.search_button = QPushButton("Pokaż")
        self.search_button.setStyleSheet(
            "background-color: green;"
            " font-size: 24px; color: white;"
            " border-radius: 8px; padding: 10px; ")
        self.search_button.setFixedSize(150, 45)
        self.search_button.clicked.connect(self.get_vehicles_list)
        self.main_layout.addWidget(self.search_button, alignment=Qt.AlignRight)

        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


    def get_vehicles_list(self):
        self.vehicle_list.clear()

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
            item.setData(Qt.UserRole, group)
            self.vehicle_list.addItem(item)
        self.adjust_list_height()

    def show_group_members(self, group):
        self.vehicle_list.clear()

        for v in group:
            display_text = (
                f"🔹 {v.brand} {v.vehicle_model}  -  "
                f"{v.cash_per_day:.2f} zł/dzień,  [{v.individual_id}]"
            )
            item = QListWidgetItem(display_text)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setData(Qt.UserRole, v)
            self.vehicle_list.addItem(item)
            self.adjust_list_height()

        # przycisk powrotu
        return_item = QListWidgetItem("↩ Wróć do listy grup")
        return_item.setData(Qt.UserRole, "return")
        self.vehicle_list.addItem(return_item)

    def handle_item_clicked(self, item):
        data = item.data(Qt.UserRole)

        if data == "return":
            self.get_vehicles_list()
            return

        if isinstance(data, list):
            self.show_group_members(data)
        elif isinstance(data, Vehicle):
            # Kliknięto pojedynczy pojazd w widoku szczegółowym
            self.vehicle_selected.emit(data)  # emituje sygnał z obiektem Vehicle
            print(f"Wybrano pojazd: {data.brand} {data.vehicle_model} [{data.individual_id}]")
        else:
            # Jeśli dane są w innej formie, np. tekst – można pominąć lub obsłużyć
            pass

    def adjust_list_height(self):
        count = self.vehicle_list.count()
        row_height = self.vehicle_list.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.vehicle_list.frameWidth()
        new_height = min(10, max(5, count)) * row_height + frame
        self.vehicle_list.setMinimumHeight(new_height)
        self.vehicle_list.setMaximumHeight(new_height)

    # def adjust_list_height(self):
    #     row_height = self.vehicle_list.sizeHintForRow(0) if self.vehicle_list.count() > 0 else 20
    #     visible_rows = max(5, min(self.vehicle_list.count(), 10))
    #     spacing = self.vehicle_list.spacing() if hasattr(self.vehicle_list, "spacing") else 2
    #     frame = 2 * self.vehicle_list.frameWidth()
    #     new_height = visible_rows * row_height + (visible_rows - 1) * spacing + frame
    #     count = self.vehicle_list.count()
    #     self.vehicle_list.setFixedHeight(new_height)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = GetVehicleWidget()
    main_window.show()
    sys.exit(app.exec())
