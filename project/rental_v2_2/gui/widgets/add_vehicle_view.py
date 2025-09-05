from PySide6.QtWidgets import (
        QWidget, QGridLayout, QFormLayout, QVBoxLayout,
        QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox, QListWidget, QListWidgetItem
    )
from PySide6.QtCore import Qt, Signal



class AddVehicleView(QWidget):

    handle_vehicles_data = Signal(list)
    update_db_request = Signal()

    def __init__(self, role="seller"):
        super().__init__()

        self.role = role

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

        title_label = QLabel("=== Dodaj nowe pojazdy na stan wypożyczalni ===.")
        title_label.setStyleSheet("font-size: 24px; color: #A9C1D9; ")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label, 1, 0, 1, 2)

        self.veh_type_combo_box = QComboBox()
        self.veh_type_combo_box.addItems(["-wybierz-", "Samochody", "Skutery", "Rowery"])
        self.veh_type = self.veh_type_combo_box.currentText()

        self.vehicle_count = QLineEdit(self)
        self.vehicle_count.setPlaceholderText("Wpisz liczbe pojazdów")
        self.veh_count_layout = QFormLayout(self)
        self.veh_count_layout.addRow("Ile pojazdów dodajesz?", self.vehicle_count)
        self.vehicle_count.editingFinished.connect(self._add_vehicle_individual)
        self.main_layout.addLayout(self.veh_count_layout, 2, 0, 1, 1)

        form1_layout = QFormLayout()
        form1_layout.addRow("Jakie pojazdy dodajesz?", self.veh_type_combo_box)
        self.veh_type_combo_box.currentTextChanged.connect(self._update_vehicle_form)
        self.main_layout.addLayout(form1_layout, 3, 0, 1, 1)

        data1_label = QLabel("Dane wspólne dla serii.")
        data1_label.setStyleSheet("font-size: 21px; color: #A9C1D9; ")
        data1_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(data1_label, 4, 0, 1, 1)

        self.data2_label = QLabel("Numer indywidualny pojazdu\n(nr rejestracyjny lub nr seryjny):")
        self.data2_label.setStyleSheet("font-size: 21px; color: #A9C1D9; ")
        self.data2_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.data2_label, 4, 1, 1, 1)
        self.data2_label.hide()

        self.veh_brand = QLineEdit()
        self.veh_brand.setMinimumWidth(135)
        self.veh_model = QLineEdit()
        self.veh_model.setMinimumWidth(135)
        self.veh_cash_per_day = QLineEdit()
        self.veh_cash_per_day.setMinimumWidth(135)
        form2_layout = QFormLayout()

        form2_layout.addRow("Producent pojazdu:", self.veh_brand)
        form2_layout.addRow("Model pjazdu:", self.veh_model)
        form2_layout.addRow("Cena najmu za dzień:", self.veh_cash_per_day)
        self.main_layout.addLayout(form2_layout, 5, 0, 1, 1)

        data2_label = QLabel("Dane indywidualne dla pojazdu.")
        data2_label.setStyleSheet("font-size: 21px; color: #A9C1D9; ")
        data2_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(data2_label, 6, 0, 1, 1)

        self.cancel1_button = QPushButton("Anuluj")
        self.cancel1_button.setMinimumSize(150, 35)
        self.cancel1_button.setStyleSheet(
            "background-color: brown;"
            "font-size: 20px; color: white;"
            " border-radius: 8px; padding: 4px;"
        )
        self.cancel1_button.clicked.connect(self._cancel_adding)
        self.main_layout.addWidget(self.cancel1_button, 8, 0, 1, 1, alignment=Qt.AlignLeft)

        self.confirm_button = QPushButton("Zatwierdź")
        self.confirm_button.setEnabled(True)
        self.confirm_button.setMinimumSize(150, 35)
        self.confirm_button.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 20px; color: white; color: white;"
            " border-radius: 8px; padding: 4px;"
        )
        self.confirm_button.clicked.connect(self._build_veh_list)
        self.main_layout.addWidget(self.confirm_button, 8, 1, 1, 1, alignment=Qt.AlignRight)

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

            self.individual_layout.addRow("Wybierz rodzaj roweru:", self.bike_typ_combo_box)
            self.individual_layout.addRow("Wybierz czy jest elektryczny:", self.bike_electric_combo_box)

        self.main_layout.addLayout(self.individual_layout, 7, 0, 1, 1)

    def _add_vehicle_individual(self):

        self.data2_label.show()

        try:
            count = int(self.vehicle_count.text().strip())
            if count <= 0:
                QMessageBox.warning(self, "Błąd", "Liczba dodawanych pojazdów musi być liczbą dodatnią")
                return
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Ilość dodawanych pojazdów musi być liczbą calkowitą")
            return

        if hasattr(self, 'individual_number_layout'):
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
            line_edit.setMinimumWidth(135)
            self.individual_number_layout.addRow(f"Nr indywidualny pojazdu {i + 1}:", line_edit)
            self.individual_number_fields.append(line_edit)

        if self.individual_number_layout.parent() is None:
            self.main_layout.addLayout(self.individual_number_layout, 5, 1, 1, 1)

    def _build_veh_list(self):

        vehicle_type = getattr(self, "vehicle_type", None)
        if vehicle_type not in ["car", "scooter", "bike"]:
            QMessageBox.warning(self, "Błąd", "Musisz wybrać typ pojazdu.")
            return

        required_fields = [
            self.veh_brand.text().strip(),
            self.veh_model.text().strip(),
            self.veh_cash_per_day.text().strip(),
        ]
        try:
            value = float(self.veh_cash_per_day.text().strip())
            if value <= 0:
                QMessageBox.warning(self, "Błąd", "Cena za dzień musi być liczbą dodatnią")
                return
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Cena za dzień musi być poprawną liczbą")
            return
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
        vehicles_data = []

        for field in self.individual_number_fields:
            text = field.text().strip()
            if self.vehicle_type == "car":

                vehicle_size = self.size_combo_box.currentText()
                if vehicle_size not in ["Miejski", "Kompaktowy", "Limuzyna", "SUV"]:
                    QMessageBox.warning(self, "Błąd", "Musisz wybrać rodzaj samochodu.")
                    return

                vehicle_fuel = self.fuel_combo_box.currentText()
                if vehicle_fuel not in ["Benzyna", "Diesel", "Hybryda", "Elektryczny"]:
                    QMessageBox.warning(self, "Błąd", "Musisz wybrać rodzaj paliwa.")
                    return

                vehicles_data.append({
                    "type": "car",
                    "brand": self.veh_brand.text().strip(),
                    "model": self.veh_model.text().strip(),
                    "cash_per_day": float(self.veh_cash_per_day.text().strip()),
                    "size": self.size_combo_box.currentText(),
                    "fuel": self.fuel_combo_box.currentText(),
                    "individual_id": text,
                })
            elif self.vehicle_type == "scooter":

                try:
                    speed = int(self.scooter_speed.text().strip())
                    if speed <= 0:
                        QMessageBox.warning(self, "Błąd", "Prędkość maksymalna musi być liczbą dodatnią")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Błąd", "Ilość dodawanych pojazdów musi być liczbą calkowitą")
                    return

                vehicles_data.append({
                    "type": "scooter",
                    "brand": self.veh_brand.text().strip(),
                    "model": self.veh_model.text().strip(),
                    "cash_per_day": float(self.veh_cash_per_day.text().strip()),
                    "max_speed": self.scooter_speed.text().strip(),
                    "individual_id": text,
                })
            elif self.vehicle_type == "bike":

                bike_type = self.bike_typ_combo_box.currentText()
                if bike_type not in ["Szosowy", "MTB", "Miejski"]:
                    QMessageBox.warning(self, "Błąd", "Musisz wybrać rodzaj roweru.")
                    return

                bike_electric = self.bike_electric_combo_box.currentText()
                if bike_electric not in ["Normalny", "Elektryczny"]:
                    QMessageBox.warning(self, "Błąd", "Musisz wybrac czy rower jest elektryczny.")
                    return

                vehicles_data.append({
                    "type": "bike",
                    "brand": self.veh_brand.text().strip(),
                    "model": self.veh_model.text().strip(),
                    "cash_per_day": float(self.veh_cash_per_day.text().strip()),
                    "bike_type": self.bike_typ_combo_box.currentText(),
                    "is_electric": (self.bike_electric_combo_box.currentText() == "Elektryczny"),
                    "individual_id": text,
                })
        self.confirm_button.setEnabled(False)
        self.handle_vehicles_data.emit(vehicles_data)

    def show_vehicles_list(self, vehicles):

        self.vehicles = vehicles

        self.confirm_label = QLabel("Sprawdź wprowadzane pojazdy czy wszystko się zgadza.")
        self.confirm_label.setStyleSheet("font-size: 21px; color: #A9C1D9; ")
        self.confirm_label.setAlignment(Qt.AlignCenter)
        self.confirm_label.show()
        self.main_layout.addWidget(self.confirm_label, 9, 0, 1, 2)

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
                vehicle_str += f"Rodzaj: {vehicle.bike_type} - {'Elektryczny' if vehicle.is_electric else 'Normalny'}"

            QListWidgetItem(vehicle_str, self.vehicles_list_widget)
            self.adjust_list_height()
        self.vehicles_list_widget.show()
        self.main_layout.addWidget(self.vehicles_list_widget, 10, 0, 1, 2)

        self.update_db_button = QPushButton("Zapisz")
        self.update_db_button.setMinimumSize(150, 35)
        self.update_db_button.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 21px; color: white; color: white;"
            " border-radius: 8px; padding: 4px;"
        )
        self.update_db_button.show()
        self.update_db_button.clicked.connect(self.update_db_request.emit)
        self.main_layout.addWidget(self.update_db_button, 11, 1, 1, 1, alignment=Qt.AlignRight)


    def show_results(self, success: bool, msg: str):
        if success:
            QMessageBox.information(self, "Sukces", msg)
        else:
            QMessageBox.critical(self, "Błąd zapisu", msg)
        self._cancel_adding()


    def _cancel_adding(self):

        if hasattr(self, "individual_number_fields"):
            for field in self.individual_number_fields:
                field.clear()

        self.vehicles = []

        self.veh_brand.clear()
        self.veh_model.clear()
        self.veh_cash_per_day.clear()
        self.vehicle_count.clear()
        self.veh_type_combo_box.setCurrentIndex(0)
        self.confirm_button.setEnabled(True)

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

        if hasattr(self, "individual_number_layout"):
            while self.individual_number_layout.count():
                item = self.individual_number_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            self.data2_label.hide()
            self.individual_number_fields = []

        if hasattr(self, "confirm_label"):
            self.confirm_label.hide()
        if hasattr(self, "vehicles_list_widget"):
            self.vehicles_list_widget.hide()
        if hasattr(self, "update_db_button"):
            self.update_db_button.hide()

    def adjust_list_height(self):
        count = self.vehicles_list_widget.count()
        row_height = self.vehicles_list_widget.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.vehicles_list_widget.frameWidth()
        new_height = min(17, max(5, count)) * row_height + frame
        self.vehicles_list_widget.setMinimumHeight(new_height)
        self.vehicles_list_widget.setMaximumHeight(new_height)


