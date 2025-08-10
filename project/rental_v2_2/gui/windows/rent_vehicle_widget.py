import sys
from datetime import date, datetime, timedelta
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox, QCalendarWidget, QHBoxLayout
    )
from PySide6.QtCore import Qt, QTimer, Signal, QDate

from services.vehicle_avability import get_unavailable_vehicle, get_available_vehicles
from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
from database.base import SessionLocal


class RentVehicleWidget(QWidget):

    def __init__(self, session = None, role = "admin", auto = False):
        super().__init__()

        self.session = session or SessionLocal()
        self.role = role
        self.auto = auto

        self.setWindowTitle("Wynajem pojazdów")

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

        self.main_layout = QGridLayout()

        self.title_label = QLabel("=== WYPOŻYCZENIE POJAZDU ===")
        self.title_label.setStyleSheet("font-size: 28px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 0, 1, 1, 3)

        self.title_label = QLabel("")
        self.title_label.setStyleSheet("font-size: 28px; color: white; ")
        self.main_layout.addWidget(self.title_label, 0, 4, 1, 1)

        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(["Wszystkie", "Samochody", "Skutery", "Rowery"])

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Jaki rodzaj pojazdu chcesz wypożyczyć:", self.type_combo_box)
        self.main_layout.addLayout(self.form_layout, 1, 1, 1, 3)

        self.title_label = QLabel("Ustaw datę początku wynajmu:")
        self.title_label.setStyleSheet("font-size: 18px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 2, 1, 1, 1)

        self.title_label = QLabel("Ustaw datę końca wynajmu:")
        self.title_label.setStyleSheet("font-size: 18px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label, 2, 3, 1, 1)



        self.calendar_start = QCalendarWidget(self)
        self.today = QDate.currentDate()
        self.calendar_start.setSelectedDate(self.today)
        self.calendar_start.setMinimumDate(self.today)
        self.calendar_start.setGridVisible(True)

        self.label_start = QLabel(f"Wybrany początek najmu: {self.today.toString('dd-MM-yyyy')}", self)

        self.calendar_start.selectionChanged.connect(self.update_start_label)

        btn_confirm = QPushButton("Zatwierdź")

        btn_confirm.clicked.connect(self.on_confirm)

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_confirm)
        # button_layout.addWidget(btn_cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar_start)
        layout.addWidget(self.label_start)
        layout.addLayout(button_layout)

        # self.setLayout(layout)
        self.main_layout.addLayout(layout, 3, 1, 1, 1)

        self.tomorrow = self.today.addDays(1)

        self.calendar_end = QCalendarWidget(self)
        self.calendar_end.setSelectedDate(self.tomorrow)
        self.calendar_end.setGridVisible(True)

        self.label_end = QLabel(f"Wybrany koniec najmu: {self.tomorrow.toString('dd-MM-yyyy')}", self)

        self.calendar_end.selectionChanged.connect(self.update_end_label)

        btn_cancel = QPushButton("Anuluj")

        btn_cancel.clicked.connect(self.cancel_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar_end)
        layout.addWidget(self.label_end)
        layout.addLayout(button_layout)

        self.main_layout.addLayout(layout, 3, 3, 1, 1)



        col_count = self.main_layout.columnCount()
        for col in range(col_count):
            self.main_layout.setColumnStretch(col, 1)

        last_row = self.main_layout.rowCount()
        self.main_layout.setRowStretch(last_row, 1)

        self.setLayout(self.main_layout)

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

    def cancel_button(self):

        self.calendar_start.setSelectedDate(self.today)
        self.label_start.setText(f"Wybrany początek najmu: {self.today.toString('dd-MM-yyyy')}")


        self.label_end.setText(f"Wybrany koniec najmu: {self.tomorrow.toString('dd-MM-yyyy')}")
        self.calendar_end.setSelectedDate(self.tomorrow)

        self.type_combo_box.setCurrentIndex(0)


    def confirm_button(self):
        """

        :return:
        """





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RentVehicleWidget()
    main_window.show()
    sys.exit(app.exec())
