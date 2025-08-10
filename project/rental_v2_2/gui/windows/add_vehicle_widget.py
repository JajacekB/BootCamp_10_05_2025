import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox, QSpacerItem, QSizePolicy
    )
from PySide6.QtCore import Qt, QTimer, Signal
from requests import session
from sqlalchemy import desc
from datetime import date

from services.id_generators import generate_vehicle_id

from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
from models.rental_history import RentalHistory
from database.base import SessionLocal


class AddVehicleWidget(QWidget):

    def __init__(self, session=None, role="client"):
        super().__init__()
        self.session =  session or SessionLocal()
        self.role = role
        self.vehicle_type = None

        self.setWindowTitle("Dodaj pojazd")

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

        self.main_layout = QGridLayout(self)

        title_label = QLabel("Dodaj nowe pojazdy na stan wypożyczalni.")
        title_label.setStyleSheet("font-size: 22px; color: white; ")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label, 0, 0, 1, 2)

        self.veh_type_combo_box = QComboBox()
        self.veh_type_combo_box.addItems(["-wybierz-", "Samochody", "Skutery", "Rowery"])
        self.veh_type = self.veh_type_combo_box.currentText()

        self.vehicle_count = QLineEdit(self)
        self.vehicle_count.setPlaceholderText("Wpisz liczbe pojazdów")
        self.veh_count_layout = QFormLayout(self)
        self.veh_count_layout.addRow("Ile pojazdów chcesz dodać?", self.vehicle_count)
        self.vehicle_count.editingFinished.connect(self._add_vehicle_individual)
        self.main_layout.addLayout(self.veh_count_layout, 1, 0, 1, 1)

        form1_layout = QFormLayout()
        form1_layout.addRow("Jakie pojazdy chcesz dodać?", self.veh_type_combo_box)
        self.veh_type_combo_box.currentTextChanged.connect(self._update_vehicle_form)
        self.main_layout.addLayout(form1_layout, 2, 0, 1, 1)

        data1_label = QLabel("Dane wspólne dla całej serii.")
        data1_label.setStyleSheet("font-size: 18px; color: white; ")
        data1_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(data1_label, 3, 0, 1, 1)

        data2_label = QLabel("Numer rejestracyjny lub seryjny.")
        data2_label.setStyleSheet("font-size: 18px; color: white; ")
        data2_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(data2_label, 3, 1, 1, 1)

        self.veh_brand = QLineEdit()
        self.veh_model = QLineEdit()
        self.veh_cash_per_day = QLineEdit()
        form2_layout = QFormLayout()
        form2_layout.addRow("Producent pojazdu:", self.veh_brand)
        form2_layout.addRow("Model pjazdu:", self.veh_model)
        form2_layout.addRow("Cena najmu za dzień:", self.veh_cash_per_day)
        self.main_layout.addLayout(form2_layout, 4, 0, 1, 1)

        data2_label = QLabel("Dane indywidualne dla typu pojazdu.")
        data2_label.setStyleSheet("font-size: 18px; color: white; ")
        data2_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(data2_label, 5, 0, 1, 1)

        self.cancel1_button = QPushButton("Anuluj")
        self.cancel1_button.setFixedSize(150, 45)
        self.cancel1_button.setStyleSheet(
            "background-color: red;"
            "font-size: 24px; color: white;"
            " border-radius: 8px; padding: 10px;"
        )
        self.cancel1_button.clicked.connect(self._cancel_adding)
        self.main_layout.addWidget(self.cancel1_button, 7, 0, 1, 1, alignment=Qt.AlignLeft)

        self.confirm_button = QPushButton("Zatwierdź")
        self.confirm_button.setFixedSize(150, 45)
        self.confirm_button.setStyleSheet(
            "background-color: green;"
            " font-size: 24px; color: white; color: white;"
            " border-radius: 8px; padding: 10px;"
        )
        self.confirm_button.clicked.connect(self._build_veh_list)
        self.main_layout.addWidget(self.confirm_button, 7, 1, 1, 1, alignment=Qt.AlignRight)

        col_count = self.main_layout.columnCount()
        for col in range(col_count):
            self.main_layout.setColumnStretch(col, 1)

        last_row = self.main_layout.rowCount()
        self.main_layout.setRowStretch(last_row, 1)

        self.setLayout(self.main_layout)

    def _update_vehicle_form(self, text):

        self.veh_type = self.veh_type_combo_box.currentText()

        if hasattr(self, "individual_layout"):
            while self.individual_layout.count():
                item = self.individual_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.main_layout.removeItem(self.individual_layout)

        self.size_combo_box = None
        self.fuel_combo_box = None
        self.scooter_speed = None
        self.bike_typ_combo_box = None
        self.bike_electric_combo_box = None

        self.individual_layout = QFormLayout()

        if self.veh_type == "Samochody":
            self.vehicle_type = "car"

            self.size_combo_box = QComboBox()
            self.size_combo_box.addItems(["-wybierz-", "Miejski", "Kompaktowy", "Limuzyna", "SUV"])

            self.fuel_combo_box = QComboBox()
            self.fuel_combo_box.addItems(["-wybierz-", "Benzyna", "Diesel", "Hybryda", "Elektryczny"])

            self.individual_layout.addRow("Wybierz klasę samochodu:", self.size_combo_box)
            self.individual_layout.addRow("Wybierz rodzaj paliwa/zasilania:", self.fuel_combo_box)

        elif self.veh_type == "Skutery":
            self.vehicle_type = "scooter"

            self.scooter_speed = QLineEdit()
            self.individual_layout.addRow("Prędkość maksymalna", self.scooter_speed)

        else:
            self.vehicle_type = "bike"

            self.bike_typ_combo_box = QComboBox()
            self.bike_typ_combo_box.addItems(["-wybierz-", "Szosowy", "MTB", "Miejski"])

            self.bike_electric_combo_box = QComboBox()
            self.bike_electric_combo_box.addItems(["-wybierz-", "Normalny", "Elektryczny"])

            self.individual_layout.addRow("Wybierz klasę samochodu:", self.bike_typ_combo_box)
            self.individual_layout.addRow("Wybierz rodzaj paliwa/zasilania:", self.bike_electric_combo_box)

        self.main_layout.addLayout(self.individual_layout, 6, 0, 1, 1)

    def _add_vehicle_individual(self):
        # Jeśli istnieje poprzedni layout lub widgety z numerami — usuń je
        if hasattr(self, 'individual_number_layout'):
            # usuń wszystkie widgety z layoutu
            while self.individual_number_layout.count():
                item = self.individual_number_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
        else:
            self.individual_number_layout = QFormLayout(self)

        self.individual_number_fields = []

        try:
            value = int(self.vehicle_count.text())
        except ValueError:
            value = 0

        for i in range(value):
            line_edit = QLineEdit()
            self.individual_number_layout.addRow(f"Numer indywidualny pojazdu {i + 1}:", line_edit)
            self.individual_number_fields.append(line_edit)

        if self.individual_number_layout.parent() is None:
            self.main_layout.addLayout(self.individual_number_layout, 4, 1, 3, 1)


    def _build_veh_list(self):

        if not self.vehicle_type or self.vehicle_type not in ["car", "scooter", "bike"]:
            QMessageBox.warning(self, "Błąd", "Wybierz typ pojazdu!")
            return

        required_fields = [
            self.veh_brand.text().strip(),
            self.veh_model.text().strip(),
            self.veh_cash_per_day.text().strip(),
        ]
        if self.vehicle_type == "car":
            required_fields.append(self.size_combo_box.currentText().strip())
            required_fields.append(self.fuel_combo_box.currentText().strip())

        elif self.vehicle_type == "scooter":
            required_fields.append(self.scooter_speed.text().strip())

        elif self.vehicle_type == "bike":
            required_fields.append(self.bike_typ_combo_box.currentText().strip())

        if hasattr(self, "individual_number_fields") and self.individual_number_fields:
            texts = []
            for field in self.individual_number_fields[:]:
                try:
                    texts.append(field.text().strip())
                except RuntimeError:
                    self.individual_number_fields.remove(field)
            required_fields.extend(texts)

        if any(not value for value in required_fields):
            QMessageBox.warning(self, "Błąd", "Uzupełnij wszystkie pola przed zatwierdzeniem.")
            return

        results = []
        self.vehicles = []
        vehicle_strs = []

        for field in self.individual_number_fields:
            self.text = field.text().strip()
            print(f"Odczytano: {self.text}")  # dodatkowa operacja
            results.append(self.text)

            if self.vehicle_type == "car":
                vehicle_id = generate_vehicle_id(self.session, "C")

                self.vehicle = Car(
                    vehicle_id=vehicle_id,
                    brand=self.veh_brand.text().strip(),
                    vehicle_model=self.veh_model.text().strip(),
                    cash_per_day=self.veh_cash_per_day.text().strip(),
                    size=self.size_combo_box.currentText(),
                    fuel_type=self.fuel_combo_box.currentText(),
                    individual_id=self.text
                )
                self.vehicle_str = (
                    f"[{self.vehicle.vehicle_id}] [{self.vehicle.individual_id}] - {self.vehicle.brand} "
                    f"{self.vehicle.vehicle_model};   {self.vehicle.cash_per_day} zł/dzień;   Typ: {self.vehicle.size};   "
                    f"Rodzaj paliwa: {self.vehicle.fuel_type}"
                )

            elif self.vehicle_type == "scooter":
                vehicle_id = generate_vehicle_id(self.session, "S")

                self.vehicle = Scooter(
                    vehicle_id=vehicle_id,
                    brand=self.veh_brand.text().strip(),
                    vehicle_model=self.veh_model.text().strip(),
                    cash_per_day=self.veh_cash_per_day.text().strip(),
                    max_speed=self.scooter_speed.text().strip(),
                    individual_id=self.text
                )

            elif self.vehicle_type == "bike":
                vehicle_id = generate_vehicle_id(self.session, "B")
                self.is_electric = self.bike_typ_combo_box.currentText() != "Normalny"

                self.vehicle = Bike(
                    vehicle_id=vehicle_id,
                    brand=self.veh_brand.text().strip(),
                    vehicle_model=self.veh_model.text().strip(),
                    cash_per_day=self.veh_cash_per_day.text().strip(),
                    bike_type=self.bike_typ_combo_box.currentText(),
                    is_electric=self.is_electric,
                    individual_id=self.text
                )

            self.session.add(self.vehicle)
            self.session.flush()
            self.vehicles.append(self.vehicle)

        confirm_label = QLabel("Sprawdź wprowadzane pojazdy czy wszystko się zgadza.")
        confirm_label.setStyleSheet("font-size: 22px; color: white; ")
        confirm_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(confirm_label, 8, 0, 1, 2)

        if hasattr(self, 'vehicles_list_widget'):
            self.main_layout.removeWidget(self.vehicles_list_widget)
            self.vehicles_list_widget.deleteLater()
            del self.vehicles_list_widget

        self.vehicles_list_widget = QListWidget()
        self.vehicles_list_widget.setStyleSheet("color: white; font-size: 16px; background-color: #333;")

        for vehicle in self.vehicles:
            vehicle_str = (
                f"[{vehicle.vehicle_id}] [{vehicle.individual_id}] - {vehicle.brand} "
                f"{vehicle.vehicle_model}; {vehicle.cash_per_day} zł/dzień; "
            )
            if self.vehicle_type == "car":
                vehicle_str += f"Typ: {vehicle.size}; Rodzaj paliwa: {vehicle.fuel_type}"
            elif self.vehicle_type == "scooter":
                vehicle_str += f"Prędkość maksymalna: {vehicle.max_speed}"
            elif self.vehicle_type == "bike":
                vehicle_str += f"Rodzaj: {vehicle.bike_type} - {'Electric' if vehicle.is_electric else 'Normalny'}"

            QListWidgetItem(vehicle_str, self.vehicles_list_widget)

        self.main_layout.addWidget(self.vehicles_list_widget, 9, 0, 1, 2)









    def _cancel_adding(self):
        # Czyścimy pola tekstowe indywidualnych numerów pojazdów
        if hasattr(self, "individual_number_fields"):
            for field in self.individual_number_fields:
                field.clear()

        # Czyścimy pola wspólne
        if hasattr(self, "veh_brand"):
            self.veh_brand.clear()

        if hasattr(self, "veh_model"):
            self.veh_model.clear()

        if hasattr(self, "veh_cash_per_day"):
            self.veh_cash_per_day.clear()

        # Czyścimy pole z liczbą pojazdów
        if hasattr(self, "vehicle_count"):
            self.vehicle_count.clear()

        # Resetujemy combo boxy do wartości domyślnych
        if hasattr(self, "veh_type_combo_box"):
            self.veh_type_combo_box.setCurrentIndex(0)

        if getattr(self, "size_combo_box", None) is not None:
            self.size_combo_box.setCurrentIndex(0)

        if getattr(self, "fuel_combo_box", None) is not None:
            self.fuel_combo_box.setCurrentIndex(0)

        if getattr(self, "bike_typ_combo_box", None) is not None:
            self.bike_typ_combo_box.setCurrentIndex(0)

        if getattr(self, "bike_electric_combo_box", None) is not None:
            self.bike_electric_combo_box.setCurrentIndex(0)

        if hasattr(self, "size_combo_box") and self.size_combo_box is not None:
            self.size_combo_box.setCurrentIndex(0)

        if hasattr(self, "fuel_combo_box") and self.fuel_combo_box is not None:
            self.fuel_combo_box.setCurrentIndex(0)

        if hasattr(self, "bike_typ_combo_box") and self.bike_typ_combo_box is not None:
            self.bike_typ_combo_box.setCurrentIndex(0)

        if hasattr(self, "bike_electric_combo_box") and self.bike_electric_combo_box is not None:
            self.bike_electric_combo_box.setCurrentIndex(0)

        # Usuwamy layout z polami indywidualnymi (numery pojazdów)
        if hasattr(self, "individual_number_layout"):
            while self.individual_number_layout.count():
                item = self.individual_number_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            self.individual_number_fields = []














if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = AddVehicleWidget()
    main_window.show()
    sys.exit(app.exec())
