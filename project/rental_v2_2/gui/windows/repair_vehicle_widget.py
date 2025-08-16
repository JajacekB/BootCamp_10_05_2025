import sys
import platform

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox, QLineEdit, QSizePolicy
    )
from PySide6.QtCore import Qt, QTimer
from datetime import date, timedelta
from gui.app_controller import AppController
from gui.windows.get_vehicle_widget import GetVehicleWidget

from database.base import SessionLocal
from models.repair_history import RepairHistory
from models.vehicle import Vehicle
from models.rental_history import RentalHistory


class RepairVehicleWidget(QWidget):
    def __init__(self, session = None, user = None, controller = None):
        super().__init__()

        self.session = session or SessionLocal()
        self.user = user
        self.controller = controller

        self.setWindowTitle("Naprawa")
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

        self. _build_ui()

    def _build_ui(self):
        self.main_layout = QVBoxLayout()

        self.get_vehicle_widget = GetVehicleWidget(self.session)
        self.get_vehicle_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.get_vehicle_widget.setMaximumHeight(385)
        self.get_vehicle_widget.vehicle_selected.connect(self.handle_list_selection)
        self.main_layout.addWidget(self.get_vehicle_widget)


        self.container_hbox0 = QWidget()
        self.hbox0 = QHBoxLayout(self.container_hbox0)

        self.comment_label_0 = QLabel(
            "Wybierz pojazd, który chcesz oddac do naprawy z listy "
            "lub wpisz jego numer katalogowy (vehicle_id):"
        )
        self.comment_label_0.setWordWrap(True)
        self.comment_label_0.setStyleSheet("font-size: 18px; ")
        self.comment_label_0.setFixedWidth(500)
        self.comment_label_0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.hbox0.addWidget(self.comment_label_0, alignment=Qt.AlignRight)

        self.input_area_0 = QLineEdit()
        self.input_area_0.setStyleSheet("font-size: 18px")
        self.input_area_0.setFixedWidth(270)
        self.input_area_0.setFixedHeight(30)
        self.input_area_0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.hbox0.addWidget(self.input_area_0)

        self.confirm_button_0_1 = QPushButton("Zatwierdź")
        self.confirm_button_0_1.setFixedSize(150,45)
        self.confirm_button_0_1.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_0_1.clicked.connect(self.handle_input_id)
        self.hbox0.addWidget(self.confirm_button_0_1)

        self.confirm_button_0_2 = QPushButton("Zatwierdź")
        self.confirm_button_0_2.setFixedSize(150, 45)
        self.confirm_button_0_2.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_0_2.hide()
        self.confirm_button_0_2.clicked.connect(self.handle_data_2)
        self.hbox0.addWidget(self.confirm_button_0_2)

        self.hbox0.addStretch()

        self.main_layout.addWidget(self.container_hbox0)


        self.container_hbox1 = QWidget()
        self.hbox1 = QHBoxLayout(self.container_hbox1)

        self.comment_label_1 = QLabel(
            "Wybierz pojazd, który chcesz oddac do naprawy z listy "
            "lub wpisz jego numer katalogowy (vehicle_id):"
        )
        self.comment_label_1.setWordWrap(True)
        self.comment_label_1.setStyleSheet("font-size: 18px; ")
        self.comment_label_1.setFixedWidth(500)
        self.comment_label_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.hbox1.addWidget(self.comment_label_1, alignment=Qt.AlignRight)

        self.combo_area_1 = QComboBox()
        self.combo_area_1.addItems(["a", "b", "c"])
        self.combo_area_1.setStyleSheet("font-size: 18px")
        self.combo_area_1.setFixedWidth(270)
        self.combo_area_1.setFixedHeight(30)
        self.combo_area_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.hbox1.addWidget(self.combo_area_1)

        self.confirm_button_1_1 = QPushButton("Zatwierdź")
        self.confirm_button_1_1.setFixedSize(150, 45)
        self.confirm_button_1_1.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_1_1.clicked.connect(self.handle_input_id)
        self.hbox1.addWidget(self.confirm_button_1_1)

        self.confirm_button_1_2 = QPushButton("Zatwierdź")
        self.confirm_button_1_2.setFixedSize(150, 45)
        self.confirm_button_1_2.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_1_2.hide()
        self.confirm_button_1_2.clicked.connect(self.handle_data_2)
        self.hbox1.addWidget(self.confirm_button_1_2)

        self.hbox1.addStretch()

        self.main_layout.addWidget(self.container_hbox1)





        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def handle_list_selection(self, vehicle):

        self.process_vehicle(vehicle)

    def handle_input_id(self):
        vehicle_id = self.input_area_1.text().capitalize()
        vehicle = self.session.query(Vehicle).filter_by(vehicle_id=vehicle_id).first()

        if vehicle:
            self.process_vehicle(vehicle)
        else:
            QMessageBox.warning(self, "Błąd", f"Nie znaleziono pojazdu o id {vehicle_id}")

    def process_vehicle(self, vehicle: Vehicle):
        self.get_vehicle_widget.vehicle_list.clear()

        print(f"Przetwarzam pojazd: {vehicle.brand} {vehicle.vehicle_model}")

        display_text = f"Wybrano: {vehicle.brand} {vehicle.vehicle_model}  [{vehicle.individual_id}]"
        item = QListWidgetItem(display_text)
        item.setFlags(Qt.NoItemFlags)
        self.get_vehicle_widget.vehicle_list.addItem(item)
        self.get_vehicle_widget.adjust_list_height()

        today = date.today()
        planned_start_date = date.today() + timedelta(days=7)
        broken_rent = self.session.query(RentalHistory).filter(
            RentalHistory.vehicle_id == vehicle.vehicle_id,
            today <= RentalHistory.planned_return_date,
            RentalHistory.start_date <= planned_start_date
        ).first()


        if not broken_rent:
            self.handle_data_1(self.session)


    def handle_data_1(self, session):
        self.comment_label_1.clear()
        self.comment_label_1.setText("Podaj ilość dni naprawy: ")
        self.input_area_1.clear()
        self.confirm_button_1.hide()
        self.confirm_button_2.show()

    def handle_data_2(self, session):
        repair_days_input = self.input_area_1.text()
        try:
            repair_days = int(repair_days_input)
            if repair_days <= 0:
                self.comment_label_1.setText("Błąd, liczba dni musi być większa od 0")
                self.input_area_1.clear()
                return
            self.repair_days = repair_days
        except ValueError:
            self.comment_label_1.setText("Błąd, Podaj prawidłową liczbę dni naprawy")
            self.input_area_1.clear()
            return

        # text_1 = f"Liczba dni w naprawie: {repair_days}"
        self.get_vehicle_widget.vehicle_list.addItem(f"Liczba dni w naprawie: {repair_days}")
        self.get_vehicle_widget.adjust_list_height()
        self.comment_label_1.clear()
















if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RepairVehicleWidget()
    main_window.showMaximized()
    sys.exit(app.exec())
