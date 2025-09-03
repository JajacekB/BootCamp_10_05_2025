from PySide6.QtWidgets import (
    QGridLayout, QFormLayout, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QComboBox, QCalendarWidget, QPushButton
)
from PySide6.QtCore import Signal, Qt, QDate


class RentVehicleView(QWidget):
    def __init__(self, current_user):
        super().__init__()

        self.current_user = current_user

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
            QCalendarWidget QHeaderView::section:horizontal {
                background-color: #444;
                color: black;
                font-weight: bold;
            }
            QCalendarWidget QHeaderView::section:vertical {
                background-color: #444;
                color: black;
            }
            QCalendarWidget QAbstractItemView {
                color: white;
            }
        """)

        self._build_ui()

    def _build_ui(self):
        self.main_layout = QGridLayout()

        self.title_label = QLabel("=== WYPOŻYCZENIE POJAZDU ===")
        self.title_label.setStyleSheet("font-size: 24px; color: #A9C1D9; ")
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

        # self.calendar_start.selectionChanged.connect(self.update_start_label)

        btn_cancel = QPushButton("Anuluj")
        # btn_cancel.clicked.connect(self.handle_cancel_button)
        btn_cancel.setStyleSheet(
            "background-color: red;"
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

        # self.calendar_end.selectionChanged.connect(self.update_end_label)

        btn_confirm = QPushButton("Zatwierdź")
        # btn_confirm.clicked.connect(self.handle_confirm_button)
        btn_confirm.setStyleSheet(
            "background-color: green;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_confirm)

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

