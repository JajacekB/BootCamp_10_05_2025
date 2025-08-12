import sys
from sqlalchemy import func, asc
from datetime import date, datetime, timedelta
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox, QCalendarWidget, QHBoxLayout
    )
from PySide6.QtCore import Qt, QTimer, Signal, QDate

from services.rental_costs import calculate_rental_cost
from services.id_generators import generate_reservation_id, generate_invoice_number
from services.vehicle_avability import get_unavailable_vehicle, get_available_vehicles
from models.user import User
from models.invoice import Invoice
from models.rental_history import RentalHistory
from models.vehicle import Vehicle, Car, Scooter, Bike
from database.base import SessionLocal


class RentVehicleWidget(QWidget):

    def __init__(self, session = None, user = None, auto = False):
        super().__init__()

        self.session = session or SessionLocal()
        self.user = user
        self.auto = auto
        self.start_date = None
        self.planned_return_date = None
        self.vehicle_type_input = None
        self.vehicle_type = None

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
        """)
        self._build_ui()

    def _build_ui(self):

        self.main_layout = QGridLayout()

        self.title_label = QLabel("=== WYPOŻYCZENIE POJAZDU ===")
        self.title_label.setStyleSheet("font-size: 24px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 0, 1, 1, 3)

        self.title_label = QLabel("")
        self.title_label.setStyleSheet("font-size: 24px; color: white; ")
        self.main_layout.addWidget(self.title_label, 0, 4, 1, 1)

        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(["Wszystkie", "Samochód", "Skuter", "Rower"])

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Jaki rodzaj pojazdu chcesz wypożyczyć:", self.type_combo_box)
        self.main_layout.addLayout(self.form_layout, 1, 1, 1, 3)

        self.title_label = QLabel("Ustaw datę początku wynajmu:")
        self.title_label.setStyleSheet("font-size: 16px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 2, 1, 1, 1)

        self.title_label = QLabel("Ustaw datę końca wynajmu:")
        self.title_label.setStyleSheet("font-size: 16px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 2, 3, 1, 1)

        self.calendar_start = QCalendarWidget(self)
        self.today = QDate.currentDate()
        # self.calendar_start.setFixedSize(300, 300)
        self.calendar_start.setSelectedDate(self.today)
        self.calendar_start.setMinimumDate(self.today)
        self.calendar_start.setGridVisible(True)

        self.label_start = QLabel(f"Wybrany początek najmu: {self.today.toString('dd-MM-yyyy')}", self)

        self.calendar_start.selectionChanged.connect(self.update_start_label)

        btn_cancel = QPushButton("Anuluj")
        btn_cancel.clicked.connect(self.handle_cancel_button)
        btn_cancel.setStyleSheet(
            "background-color: green;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar_start)
        layout.addWidget(self.label_start)
        layout.addLayout(button_layout)
        self.main_layout.addLayout(layout, 3, 1, 1, 1)

        self.tomorrow = self.today.addDays(1)

        self.calendar_end = QCalendarWidget(self)
        # self.calendar_end.setFixedSize(300, 300)
        self.calendar_end.setSelectedDate(self.tomorrow)
        self.calendar_end.setGridVisible(True)

        self.label_end = QLabel(f"Wybrany koniec najmu: {self.tomorrow.toString('dd-MM-yyyy')}", self)

        self.calendar_end.selectionChanged.connect(self.update_end_label)

        btn_confirm = QPushButton("Zatwierdź")
        btn_confirm.clicked.connect(self.handle_confirm_button)
        btn_confirm.setStyleSheet(
            "background-color: red;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_confirm)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar_end)
        layout.addWidget(self.label_end)
        layout.addLayout(button_layout)
        self.main_layout.addLayout(layout, 3, 3, 1, 1)

        self.list_widget = QListWidget()
        font = self.list_widget.font()
        font.setFamily("Consolas")  # "Courier New", "Consolas", "DejaVu Sans Mono", "Monospace", "Monaco"
        self.list_widget.setFont(font)
        self.list_widget.itemClicked.connect(
            lambda item: self.handle_single_vehicle_click(item)
            if item.data(Qt.UserRole) is not None else None
        )
        self.main_layout.addWidget(self.list_widget, 4, 1, 1, 3)

        self.main_layout.addWidget(self._build_dynamic_area(), 5, 0, 1, 5)


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
        # self.btn_rent_cancel.clicked.connect(self.handle_rent_cancel_button)
        self.btn_rent_cancel.setStyleSheet(
            "background-color: green;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        self.btn_rent_accept = QPushButton("Wypożycz")
        self.btn_rent_accept.clicked.connect(self.handle_rent_accept_button)
        self.btn_rent_accept.setStyleSheet(
            "background-color: red;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)

        self.btn_rent_final_cancel = QPushButton("Anuluj")
        # self.btn_rent_cancel.clicked.connect(self.handle_rent_cancel_button)
        self.btn_rent_final_cancel.setStyleSheet(
            "background-color: green;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        self.btn_rent_final_accept = QPushButton("Zakończ")
        self.btn_rent_final_accept.clicked.connect(self.handle_rent_final_accept_button)
        self.btn_rent_final_accept.setStyleSheet(
            "background-color: red;"
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

    def handle_cancel_button(self):

        self.calendar_start.setSelectedDate(self.today)
        self.label_start.setText(f"Wybrany początek najmu: {self.today.toString('dd-MM-yyyy')}")


        self.label_end.setText(f"Wybrany koniec najmu: {self.tomorrow.toString('dd-MM-yyyy')}")
        self.calendar_end.setSelectedDate(self.tomorrow)

        self.type_combo_box.setCurrentIndex(0)


    def handle_confirm_button(self):
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
        vehicles_to_rent = get_available_vehicles(
            self.session, self.start_date, self.planned_return_date, self.vehicle_type
        )

        if self.vehicle_type == "all":
            self.list_widget.clear()

            vehicles_to_rent = get_available_vehicles(self.session, self.start_date, self.planned_return_date)

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
                # f"|{index:>4}|{v_type:>11}|{brand:<17}|{model:<17}|{formatted_price:>15}|{len(scooter):^9}|"
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, vehicle)
                self.list_widget.addItem(item)

        elif self.vehicle_type == "car":
            self.list_widget.clear()

            vehicles_to_rent = get_available_vehicles(
                self.session, self.start_date, self.planned_return_date, self.vehicle_type
            )
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

            vehicles_to_rent = get_available_vehicles(
                self.session, self.start_date, self.planned_return_date, self.vehicle_type
            )
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

            vehicles_to_rent = get_available_vehicles(
                self.session, self.start_date, self.planned_return_date, self.vehicle_type
            )
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


    def handle_single_vehicle_click(self, item):
        if item.data(Qt.UserRole) == "header":
            return  # ignorujemy kliknięcie w nagłówek
        group = item.data(Qt.UserRole)
        if not isinstance(group, list) or not group:
            return

        matching_ids = [v.id for v in group]

        result = self.session.query(
            Vehicle,
            func.count(RentalHistory.id).label("rental_count")
        ).outerjoin(RentalHistory).filter(
            Vehicle.id.in_(matching_ids)
        ).group_by(Vehicle.id).order_by("rental_count").first()

        if result:
            self.chosen_vehicle, rental_count = result
        else:
            self.chosen_vehicle = group[0] if group else None
            rental_count = 0

        self.append_layout.addWidget(self.info_0_label, 0, 0, 1, 1)
        self.append_layout.addWidget(self.info_label, 0, 1, 1, 3)
        self.append_layout.addWidget(self.info_5_label, 0, 5, 1, 1)

        self.info_label.setText(
            f"Czy na pewno chcesz wypozyczyć ten pojazd?\n\n{self.chosen_vehicle.get_display_info()}"
        )
        self.append_layout.addWidget(self.btn_rent_cancel, 1, 1, 1, 1)
        self.append_layout.addWidget(self.btn_rent_accept, 1, 3, 1, 1)

    def handle_rent_accept_button(self, item):
        # self.user = self.session.query(User).filter(User.role == "admin").first()

        rent_days = (self.planned_return_date - self.start_date).days
        self.base_cost = rent_days * self.chosen_vehicle.cash_per_day
        self.total_cost, discount_value, discount_type = calculate_rental_cost(
            self.user, self.chosen_vehicle.cash_per_day, rent_days
        )
        total_cost_str = (
            f"Całkowity koszt {self.total_cost} zł\n"
            f"Kwota bazowa {self.base_cost} zł, udzielone rabaty {discount_value} zł {discount_type}"
        )
        self.append_layout.addWidget(self.summary_label, 2, 1, 1, 3)

        self.summary_label.setText(
            f"Całkowity koszt {self.total_cost} zł\n"
            f"Kwota bazowa {self.base_cost} zł, udzielone rabaty {discount_value}% {discount_type}"
        )
        self.append_layout.addWidget(self.btn_rent_final_cancel, 3, 1, 1, 1)
        self.append_layout.addWidget(self.btn_rent_final_accept, 3, 3, 1, 1)

    def handle_rent_final_accept_button(self):
        try:
            reservation_id = generate_reservation_id(self.session)
            invoice_number = generate_invoice_number(self.session, self.planned_return_date)

            # Aktualizacja pojazdu
            self.chosen_vehicle.is_available = False
            self.chosen_vehicle.borrower_id = self.user.id
            self.chosen_vehicle.return_date = self.planned_return_date
            self.session.add(self.chosen_vehicle)

            # Aktualizacja historii wypożyczeń
            rental = RentalHistory(
                reservation_id=reservation_id,
                user_id=self.user.id,
                vehicle_id=self.chosen_vehicle.id,
                start_date=self.start_date,
                planned_return_date=self.planned_return_date,
                base_cost=self.base_cost,
                total_cost=self.total_cost
            )
            self.session.add(rental)
            self.session.flush()

            # Faktura
            invoice = Invoice(
                invoice_number=invoice_number,
                rental_id=rental.id,
                amount=self.total_cost,
                issue_date=self.planned_return_date
            )

            self.session.add_all([invoice])
            self.session.commit()

            QMessageBox.information(
                self,
                "Rezerwacja zakończona",
                f"\n✅ Zarezerwowałeś {self.chosen_vehicle.brand} {self.chosen_vehicle.vehicle_model} "
                f"od {self.start_date} do {self.planned_return_date}."
                "\nMiłej jazdy!"
            )

        except Exception as e:
            self.session.rollback()
            # ❌ Błąd
            QMessageBox.critical(
                self,
                "Błąd rezerwacji",
                f"Wystąpił problem podczas zapisu rezerwacji.\nSzczegóły: {e}"
            )



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RentVehicleWidget()
    main_window.show()
    sys.exit(app.exec())
