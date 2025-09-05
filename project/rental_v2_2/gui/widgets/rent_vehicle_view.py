import platform
from datetime import date
from collections import defaultdict
from PySide6.QtWidgets import (
    QGridLayout, QFormLayout, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QComboBox, QCalendarWidget, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QLineEdit
)
from PySide6.QtGui import QTextCharFormat
from PySide6.QtCore import Signal, Qt, QDate


class RentVehicleView(QWidget):

    handle_confirm_button = Signal(object, object, str)
    handle_single_vehicle = Signal(list)
    handle_accept_button = Signal(str)
    handle_rent_condition_accept = Signal(object)

    def __init__(self, current_role):
        super().__init__()

        self.current_role = current_role
        self.start_date = None
        self.planned_return_date = None
        self.vehicle_type_input = None
        self.vehicle_type = None
        self.client_info = None

        self.setWindowTitle("Wynajem pojazdów")

        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e; /* Ciemne tło dla całego widgetu */
                color: #eee; /* Jasny kolor tekstu */
                font-size: 14px;
            }
            QPushButton {
                background-color: #555;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                font-size: 14px;
            }            
            QCalendarWidget {
                font-size: 10px;
            }
        """)

        self._build_ui()

    def _build_ui(self):

        self.main_layout = QGridLayout()

        if self.current_role in ["admin", "seller"]:
            chose_layout = QFormLayout()
            self.client_info_input = QLineEdit()
            self.client_info_input.setPlaceholderText("Zostaw puste pole jeśli wypozyczasz dla siebie!")
            chose_layout.addRow("Podaj numer klienta:", self.client_info_input)

            self.main_layout.addLayout(chose_layout, 0, 1, 1, 3)

        self.title_label = QLabel("=== WYPOŻYCZENIE POJAZDU ===")
        self.title_label.setStyleSheet("font-size: 24px; color: #A9C1D9; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 1, 1, 1, 3)

        self.title_label = QLabel("")
        self.title_label.setStyleSheet("font-size: 24px; color: white; ")
        self.main_layout.addWidget(self.title_label, 1, 4, 1, 1)

        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(["Wszystkie", "Samochód", "Skuter", "Rower"])

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Jaki rodzaj pojazdu chcesz wypożyczyć:", self.type_combo_box)
        self.main_layout.addLayout(self.form_layout, 2, 1, 1, 3)

        self.title_label = QLabel("Ustaw datę początku wynajmu:")
        self.title_label.setStyleSheet("font-size: 16px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 3, 1, 1, 1)

        self.title_label = QLabel("Ustaw datę końca wynajmu:")
        self.title_label.setStyleSheet("font-size: 16px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 3, 3, 1, 1)

        self.calendar_start = QCalendarWidget()
        self.today = QDate.currentDate()
        # self.calendar_start.setMinimumSize(300, 200)
        self.calendar_start.setSelectedDate(self.today)
        self.calendar_start.setMinimumDate(self.today)
        self.calendar_start.setGridVisible(True)
        fmt = QTextCharFormat()
        fmt.setForeground(Qt.black)
        self.calendar_start.setHeaderTextFormat(fmt)

        self.label_start = QLabel(f"Wybrany początek najmu: {self.today.toString('dd-MM-yyyy')}", self)

        self.calendar_start.selectionChanged.connect(self.update_start_label)

        btn_cancel = QPushButton("Anuluj")
        btn_cancel.clicked.connect(self.handle_cancel_button)
        btn_cancel.setStyleSheet(
            "background-color: brown;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar_start)
        layout.addWidget(self.label_start)
        layout.addLayout(button_layout)
        self.main_layout.addLayout(layout, 4, 1, 1, 1)

        self.tomorrow = self.today.addDays(1)

        self.calendar_end = QCalendarWidget()
        # self.calendar_end.setMinimumSize(300, 200)
        self.calendar_end.setSelectedDate(self.tomorrow)
        self.calendar_end.setGridVisible(True)
        fmt = QTextCharFormat()
        fmt.setForeground(Qt.black)
        self.calendar_end.setHeaderTextFormat(fmt)

        self.label_end = QLabel(f"Wybrany koniec najmu: {self.tomorrow.toString('dd-MM-yyyy')}", self)

        self.calendar_end.selectionChanged.connect(self.update_end_label)

        btn_confirm = QPushButton("Zatwierdź")
        btn_confirm.clicked.connect(self._on_click_confirm_button)
        btn_confirm.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_confirm)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar_end)
        layout.addWidget(self.label_end)
        layout.addLayout(button_layout)
        self.main_layout.addLayout(layout, 4, 3, 1, 1)

        self.list_widget = QListWidget()
        font = self.list_widget.font()
        system = platform.system()
        if system == "Windows":
            font.setFamily("Consolas")
        elif system == "Darwin":  # macOS
            font.setFamily("Menlo")
        else:  # Linux i inne
            font.setFamily("DejaVu Sans Mono")

        self.list_widget.setFont(font)
        self.list_widget.itemClicked.connect(
            lambda item: self.on_click_single_vehicle(item)
            if item.data(Qt.UserRole) is not None else None
        )
        self.main_layout.addWidget(self.list_widget, 5, 1, 1, 3)

        self.main_layout.addWidget(self._build_dynamic_area(), 6, 0, 1, 5)

        col_count = self.main_layout.columnCount()
        for col in range(col_count):
            self.main_layout.setColumnStretch(col, 1)

        last_row = self.main_layout.rowCount()
        self.main_layout.setRowStretch(last_row, 1)

        self.setLayout(self.main_layout)



    def _build_dynamic_area(self):
        # 1. Tworzę kontener QWidget
        self.dynamic_widget = QWidget()

        # 2. Wkładam w niego QGridLayout
        self.append_layout = QGridLayout()
        self.append_layout.setAlignment(Qt.AlignTop)
        self.dynamic_widget.setLayout(self.append_layout)

        self.info_0_label = QLabel()
        self.info_0_label.setWordWrap(True)

        self.info_label = QLabel()
        self.info_label.setWordWrap(True)

        self.info_5_label = QLabel()
        self.info_5_label.setWordWrap(True)

        self.btn_rent_cancel = QPushButton("Anuluj")
        self.btn_rent_cancel.clicked.connect(self.handle_cancel_button)
        self.btn_rent_cancel.setStyleSheet(
            "background-color: brown;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        self.btn_rent_accept = QPushButton("Wypożycz")
        self.btn_rent_accept.clicked.connect(self._on_click_rent_accept_button)
        self.btn_rent_accept.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)


        self.btn_rent_final_cancel = QPushButton("Anuluj")
        self.btn_rent_final_cancel.clicked.connect(self.handle_cancel_button)
        self.btn_rent_final_cancel.setStyleSheet(
            "background-color: brown;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        self.btn_rent_final_accept = QPushButton("Zakończ")
        self.btn_rent_final_accept.clicked.connect(self._on_click_rent_conditions_accept)
        self.btn_rent_final_accept.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        return self.dynamic_widget

    def update_start_label(self):
        start_date = self.calendar_start.selectedDate()
        self.label_start.setText(f"Wybrany początek najmu: {start_date.toString('dd-MM-yyyy')}")

        min_end_date = start_date.addDays(1)
        self.calendar_end.setMinimumDate(min_end_date)  # Ograniczamy kalendarz końcowy

        if self.calendar_end.selectedDate() < min_end_date:
            self.calendar_end.setSelectedDate(min_end_date)
            self.label_end.setText(f"Wybrany koniec najmu: {min_end_date.toString('dd-MM-yyyy')}")

    def update_end_label(self):
        end_date = self.calendar_end.selectedDate()
        start_date = self.calendar_start.selectedDate()
        min_end_date = start_date.addDays(1)

        if end_date < min_end_date:
            self.calendar_end.setSelectedDate(min_end_date)
            end_date = min_end_date

        self.label_end.setText(f"Wybrany koniec najmu: {end_date.toString('dd-MM-yyyy')}")

    def _on_click_confirm_button(self):
        start_date_input = self.calendar_start.selectedDate()
        self.start_date = date(start_date_input.year(), start_date_input.month(), start_date_input.day())

        end_date_input = self.calendar_end.selectedDate()
        self.planned_return_date = date(end_date_input.year(), end_date_input.month(), end_date_input.day())

        self.vehicle_type_input = self.type_combo_box.currentText()

        vehicle_type_map = {
            "Wszystkie": "all",
            "Samochód": "car",
            "Skuter": "scooter",
            "Rower": "bike"
        }
        self.vehicle_type = vehicle_type_map.get(self.vehicle_type_input)

        self.handle_confirm_button.emit(self.start_date, self.planned_return_date, self.vehicle_type)

    def show_vehicle_for_rent(self, vehicles_to_rent):

        if self.vehicle_type == "all":
            self.list_widget.clear()

            vehicles_sorted = sorted(
                vehicles_to_rent,
                key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model)
            )
            grouped = defaultdict(list)
            for v in (vehicles_sorted):
                key = (v.brand, v.vehicle_model, v.cash_per_day, v.type)
                grouped[key].append(v)

            header = f"|{'#':>4}| {'Typ':<9}| {'Marka':<15}| {'Model':<15}|{'Cena':>13} |"
            self.list_widget.addItem(header)
            self.list_widget.addItem("-" * len(header))

            for index, ((brand, model, price, v_type), vehicle) in enumerate(grouped.items(), start=1):
                formatted_price = f"{price:.2f} zł"

                display_text = (
                    f"|{index:>4}| {v_type:<9}|{brand:<15} | {model:<15}|{formatted_price:>13} |"
                )
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, vehicle)
                self.list_widget.addItem(item)

        elif self.vehicle_type == "car":
            self.list_widget.clear()

            vehicles_sorted = sorted(
                vehicles_to_rent,
                key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model, v.fuel_type)
            )
            grouped = defaultdict(list)
            for v in (vehicles_sorted):
                key = (v.brand, v.vehicle_model, v.cash_per_day, v.size, v.fuel_type)
                grouped[key].append(v)

            header = f"|{'#':>4} | {'Marka':<11}| {'Model':<11}| {'Rodzaj':<11}| {'Paliwo':<11}|{'Cena':>13} |"
            self.list_widget.addItem(header)
            self.list_widget.addItem("-" * len(header))

            for index, ((brand, model, price, size, fuel_type), cars) in enumerate(grouped.items(), start=1):
                formatted_price = f"{price:.2f} zł"

                display_text = (
                    f"|{index:>4} | {brand:<11}| {model:<11}| {size:<11}| {fuel_type:<11}|{formatted_price:>13} |"
                )
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, cars)
                self.list_widget.addItem(item)

        elif self.vehicle_type == "scooter":
            self.list_widget.clear()

            vehicles_sorted = sorted(
                vehicles_to_rent,
                key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model)
            )
            grouped = defaultdict(list)
            for v in (vehicles_sorted):
                key = (v.brand, v.vehicle_model, v.cash_per_day, v.max_speed)
                grouped[key].append(v)

            header = f"|{'#':>4} | {'Marka':<11}| {'Model':<11}|{'Prędkość max':>13} |{'Cena':>13} |"
            self.list_widget.addItem(header)
            self.list_widget.addItem("-" * len(header))

            for index, ((brand, model, price, max_speed), scooter) in enumerate(grouped.items(), start=1):
                formatted_price = f"{price:.2f} zł"

                display_text = (
                    f"|{index:>4} | {brand:<11}| {model:<11}|{max_speed:>13} |{formatted_price:>13} |"
                )
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, scooter)
                self.list_widget.addItem(item)

        elif self.vehicle_type == "bike":
            self.list_widget.clear()

            vehicles_sorted = sorted(
                vehicles_to_rent,
                key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model)
            )
            grouped = defaultdict(list)
            for v in (vehicles_sorted):
                key = (v.brand, v.vehicle_model, v.cash_per_day, v.bike_type, v.is_electric)
                grouped[key].append(v)

            header = f"|{'#':>4}| {'Marka':<13}| {'Model':<15}| {'Rodzaj':<23}|{'Cena':>11} |"
            self.list_widget.addItem(header)
            self.list_widget.addItem("-" * len(header))

            for index, ((brand, model, price, bike_type, is_electric), bike) in enumerate(grouped.items(), start=1):
                formatted_price = f"{price:.2f} zł"
                if is_electric:
                    bike_variety = f"{bike_type} - elektryczny"
                else:
                    bike_variety = f"{bike_type} - klasyczny"

                display_text = (
                    f"|{index:>4}| {brand:<13}| {model:<15}| {bike_variety:23}|{formatted_price:>11} |"
                )
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, bike)
                self.list_widget.addItem(item)

        if not vehicles_to_rent:
            print("\n🚫 Brak pasujących pojazdów.")
            return

    def on_click_single_vehicle(self, item):
        if item.data(Qt.UserRole) == "header":
            return  # ignorujemy kliknięcie w nagłówek
        self.group = item.data(Qt.UserRole)
        if not isinstance(self.group, list) or not self.group:
            return

        self.handle_single_vehicle.emit(self.group)

    def show_chosen_vehicle(self, chosen_vehicle, rental_count):

        self.info_0_label.show()
        self.info_label.show()
        self.info_5_label.show()
        self.append_layout.addWidget(self.info_0_label, 1, 0, 1, 1)
        self.append_layout.addWidget(self.info_label, 1, 1, 1, 3)
        self.append_layout.addWidget(self.info_5_label, 1, 5, 1, 1)

        self.info_label.setText(
            f"Czy na pewno chcesz wypozyczyć ten pojazd?\n\n{chosen_vehicle.get_display_info()}"
        )
        self.btn_rent_cancel.show()
        self.append_layout.addWidget(self.btn_rent_cancel, 2, 1, 1, 1)
        self.btn_rent_accept.show()
        self.append_layout.addWidget(self.btn_rent_accept, 2, 3, 1, 1)

    def _on_click_rent_accept_button(self, item):
        self.client_info = self.client_info_input.text()
        print(f"_on_click_rent_accept_button says {self.client_info=}")
        self.handle_accept_button.emit(self.client_info)

    def show_rental_cost(self, total_cost, discount_value, discount_type, total_cost_str, user):

        self.user = user
        self.total_cost = total_cost
        self.summary_label.show()
        self.append_layout.addWidget(self.summary_label, 3, 1, 1, 3)

        self.summary_label.setText(total_cost_str)
        self.btn_rent_final_cancel.show()
        self.append_layout.addWidget(self.btn_rent_final_cancel, 4, 1, 1, 1)
        self.btn_rent_final_accept.show()
        self.append_layout.addWidget(self.btn_rent_final_accept, 4, 3, 1, 1)

    def _on_click_rent_conditions_accept(self):
        self.handle_rent_condition_accept.emit(self.user)

    def show_final_information(self, success, msg):

        if success:
            QMessageBox.information(
                self,
                "Rezerwacja zakończona",
                f"{msg}"
            )
            self.handle_cancel_button()

        else:
            QMessageBox.critical(
                self,
                "Błąd rezerwacji",
                f"{msg}"
            )
            self.handle_cancel_button()

    def handle_cancel_button(self):
        # reset kalendarza
        self.calendar_start.setSelectedDate(self.today)
        self.label_start.setText(f"Wybrany początek najmu: {self.today.toString('dd-MM-yyyy')}")
        self.label_end.setText(f"Wybrany koniec najmu: {self.tomorrow.toString('dd-MM-yyyy')}")
        self.calendar_end.setSelectedDate(self.tomorrow)
        self.type_combo_box.setCurrentIndex(0)
        # Czyszczenie listy
        self.list_widget.clear()
        # Czyszczenie podsumowania i przysisków sterujacych
        self.info_0_label.setText("")
        self.info_0_label.hide()
        self.info_label.setText("")
        self.info_label.hide()
        self.btn_rent_cancel.hide()
        self.btn_rent_accept.hide()
        self.info_5_label.setText("")
        self.info_5_label.hide()
        # Czyszczenie pytania o potwierdzenie i przucsków steujacych
        self.summary_label.setText("")
        self.summary_label.hide()
        self.btn_rent_final_cancel.hide()
        self.btn_rent_final_accept.hide()






    def adjust_list_height(self):
        count = self.list_widget.count()
        row_height = self.list_widget.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.list_widget.frameWidth()
        new_height = min(10, max(5, count)) * row_height + frame
        self.list_widget.setMinimumHeight(new_height)
        self.list_widget.setMaximumHeight(new_height)