import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox
    )
from PySide6.QtCore import Qt, QTimer, Signal
from requests import session
from sqlalchemy import desc
from datetime import date

from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
from models.rental_history import RentalHistory
from database.base import SessionLocal


class AddVehicleWidget(QWidget):

    def __init__(self, session=None, role="client"):
        super().__init__()
        self.session =  session or SessionLocal()
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

        title_label = QLabel("Dodaj nowe pojazdy na stan wypożyczalni.")
        title_label.setStyleSheet("font-size: 22px; color: white; ")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label, 0, 0, 1, 2)

        self.veh_type_combo_box = QComboBox()
        self.veh_type_combo_box.addItems(["Samochody", "Skutery", "Rowery"])
        self.veh_type = self.veh_type_combo_box.currentText()

        self.vehicle_count = QLineEdit(self)
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
        self.veh_size = QLineEdit()
        self.veh_fuel = QLineEdit()
        form2_layout = QFormLayout()
        form2_layout.addRow("Producent pojazdu:", self.veh_brand)
        form2_layout.addRow("Model pjazdu:", self.veh_size)
        form2_layout.addRow("Cena najmu za dzień:", self.veh_fuel)
        self.main_layout.addLayout(form2_layout, 4, 0, 1, 1)

        data2_label = QLabel("Dane indywidualne dla typu pojazdu.")
        data2_label.setStyleSheet("font-size: 18px; color: white; ")
        data2_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(data2_label, 5, 0, 1, 1)


        self.setLayout(self.main_layout)

    def _update_vehicle_form(self, text):

        self.veh_type = self.veh_type_combo_box.currentText()

        if hasattr(self, "individual_layout"):
            while self.individual_layout.count():
                item = self.individual_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.main_layout.removeItem(self.individual_layout)

        self.individual_layout = QFormLayout()

        if self.veh_type == "Samochody":
            self.vehicle_type = "car"

            self.size_combo_box = QComboBox()
            self.size_combo_box.addItems(["Miejski", "Kompaktowy", "Limuzyna", "SUV"])

            self.fuel_combo_box = QComboBox()
            self.fuel_combo_box.addItems(["Benzyna", "Diesel", "Hybryda", "Elektryczny"])

            self.individual_layout.addRow("Wybierz klasę samochodu:", self.size_combo_box)
            self.individual_layout.addRow("Wybierz rodzaj paliwa/zasilania:", self.fuel_combo_box)

        elif self.veh_type == "Skutery":
            self.vehicle_type = "scooter"

            self.scooter_speed = QLineEdit()
            self.individual_layout.addRow("Prędkość maksymalna", self.scooter_speed)

        else:
            self.vehicle_type = "bike"

            self.bike_typ_combo_box = QComboBox()
            self.bike_typ_combo_box.addItems(["Szosowy", "MTB", "Miejski"])

            self.bike_electric_combo_box = QComboBox()
            self.bike_electric_combo_box.addItems(["Normalny", "Elektryczny"])

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
            # opcjonalnie: usuń layout z głównego layoutu jeśli trzeba

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

    def get_individual_numbers(self):
        return [field.text() for field in self.individual_number_fields]




        # for item_text in menu_list:
        #     button = QPushButton(item_text)
        #     button.setFixedSize(255, 31)
        #     button.setStyleSheet("color: white; border-radius: 8px; padding-left: 10px;")
        #     menu_layout.addWidget(button, alignment=Qt.AlignCenter)
        #     command_num = item_text.split(".")[0]
        #     button.clicked.connect(lambda checked, num=command_num: self._on_dynamic_button_clicked(num))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = AddVehicleWidget()
    main_window.show()
    sys.exit(app.exec())
