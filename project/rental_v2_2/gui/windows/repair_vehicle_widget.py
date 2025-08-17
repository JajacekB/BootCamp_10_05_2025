import sys
from sqlalchemy import func
from datetime import date, timedelta

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox, QLineEdit, QSizePolicy
    )
from PySide6.QtCore import Qt, QTimer

from gui.windows.get_vehicle_widget import GetVehicleWidget
from models.user import User
from models.vehicle import Vehicle
from database.base import SessionLocal
from models.repair_history import RepairHistory
from models.rental_history import RentalHistory
from services.user_service import get_users_by_role
from services.id_generators import generate_repair_id


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
        # self.confirm_button_0_2.clicked.connect(self.handle_data_2)
        self.hbox0.addWidget(self.confirm_button_0_2)

        self.hbox0.addStretch()

        self.main_layout.addWidget(self.container_hbox0)


        self.container_hbox1 = QWidget()
        self.hbox1 = QHBoxLayout(self.container_hbox1)

        self.comment_label_1 = QLabel(
            "Wybierz warsztat do którego oddajesz pojazd:"
        )
        self.comment_label_1.setWordWrap(True)
        self.comment_label_1.setStyleSheet("font-size: 18px; ")
        self.comment_label_1.setFixedWidth(500)
        self.comment_label_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.hbox1.addWidget(self.comment_label_1, alignment=Qt.AlignRight)

        self.combo_area_1 = QComboBox()
        self.combo_area_1.addItems([])
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
        self.confirm_button_1_1.hide()
        # self.confirm_button_1_1.clicked.connect(self.handle_input_id)
        self.hbox1.addWidget(self.confirm_button_1_1)

        self.confirm_button_1_2 = QPushButton("Zatwierdź")
        self.confirm_button_1_2.setFixedSize(150, 45)
        self.confirm_button_1_2.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_1_2.hide()
        # self.confirm_button_1_2.clicked.connect(self.handle_data_2)
        self.hbox1.addWidget(self.confirm_button_1_2)

        self.hbox1.addStretch()
        self.container_hbox1.hide()

        self.main_layout.addWidget(self.container_hbox1)


        self.container_hbox2 = QWidget()
        self.hbox2 = QHBoxLayout(self.container_hbox2)

        self.comment_label_2 = QLabel(
            "Podaj koszt naprawy liczony za jeden dzień:"
        )
        self.comment_label_2.setWordWrap(True)
        self.comment_label_2.setStyleSheet("font-size: 18px; ")
        self.comment_label_2.setFixedWidth(500)
        self.comment_label_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.hbox2.addWidget(self.comment_label_2, alignment=Qt.AlignRight)

        self.input_area_2 = QLineEdit()
        self.input_area_2.setStyleSheet("font-size: 18px")
        self.input_area_2.setFixedWidth(270)
        self.input_area_2.setFixedHeight(30)
        self.input_area_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.hbox2.addWidget(self.input_area_2)

        self.confirm_button_2_1 = QPushButton("Zatwierdź")
        self.confirm_button_2_1.setFixedSize(150, 45)
        self.confirm_button_2_1.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_2_1.hide()
        # self.confirm_button_2_1.clicked.connect(self.handle_data_1)
        self.hbox2.addWidget(self.confirm_button_2_1)

        self.confirm_button_2_2 = QPushButton("Zatwierdź")
        self.confirm_button_2_2.setFixedSize(150, 45)
        self.confirm_button_2_2.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_2_2.hide()
        # self.confirm_button_2_2.clicked.connect(self.handle_data_2)
        self.hbox2.addWidget(self.confirm_button_2_2)

        self.hbox2.addStretch()
        self.container_hbox2.hide()

        self.main_layout.addWidget(self.container_hbox2)


        self.container_hbox3 = QWidget()
        self.hbox3 = QHBoxLayout(self.container_hbox3)

        self.comment_label_3 = QLabel(
            "Opisz krótko zakres naprawy:"
        )
        self.comment_label_3.setWordWrap(True)
        self.comment_label_3.setStyleSheet("font-size: 18px; ")
        self.comment_label_3.setFixedWidth(500)
        self.comment_label_3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.hbox3.addWidget(self.comment_label_3, alignment=Qt.AlignRight)

        self.input_area_3 = QLineEdit()
        self.input_area_3.setStyleSheet("font-size: 18px")
        self.input_area_3.setFixedWidth(270)
        self.input_area_3.setFixedHeight(30)
        self.input_area_3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.hbox3.addWidget(self.input_area_3)

        self.confirm_button_3_1 = QPushButton("Zatwierdź")
        self.confirm_button_3_1.setFixedSize(150, 45)
        self.confirm_button_3_1.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_3_1.clicked.connect(self.handle_data_1)
        self.hbox3.addWidget(self.confirm_button_3_1)

        self.confirm_button_3_2 = QPushButton("Zatwierdź")
        self.confirm_button_3_2.setFixedSize(150, 45)
        self.confirm_button_3_2.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_3_2.hide()
        # self.confirm_button_2_2.clicked.connect(self.handle_data_2)
        self.hbox3.addWidget(self.confirm_button_3_2)

        self.hbox3.addStretch()
        self.container_hbox3.hide()

        self.main_layout.addWidget(self.container_hbox3)





        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def handle_list_selection(self, vehicle):

        self.process_vehicle(vehicle)

    def handle_input_id(self):
        vehicle_id = self.input_area_0.text().capitalize()
        vehicle = self.session.query(Vehicle).filter_by(vehicle_id=vehicle_id).first()

        if vehicle:
            self.process_vehicle(vehicle)
        else:
            QMessageBox.warning(self, "Błąd", f"Nie znaleziono pojazdu o id {vehicle_id}")

    def process_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.get_vehicle_widget.vehicle_list.clear()

        print(f"Przetwarzam pojazd: {vehicle.brand} {vehicle.vehicle_model}")

        display_text = f"Wybrano: {self.vehicle.brand} {self.vehicle.vehicle_model}  [{self.vehicle.individual_id}]"
        item = QListWidgetItem(display_text)
        item.setFlags(Qt.NoItemFlags)
        self.get_vehicle_widget.vehicle_list.addItem(item)
        self.get_vehicle_widget.adjust_list_height()

        self.workshops = get_users_by_role(self.session, "workshop")
        for w in self.workshops:
            workshop_name = f"{w.first_name} {w.last_name}"
            self.combo_area_1.addItem(workshop_name, userData=w)

        self.comment_label_0.clear()
        self.comment_label_0.setText("Podaj ilość dni naprawy: ")
        self.input_area_0.clear()
        self.confirm_button_0_1.hide()
        self.confirm_button_0_2.hide()

        self.container_hbox1.show()
        self.confirm_button_1_1.hide()
        self.confirm_button_1_2.hide()

        self.container_hbox2.show()
        self.confirm_button_2_1.hide()
        self.confirm_button_2_2.hide()

        self.container_hbox3.show()
        self.confirm_button_3_1.show()
        self.confirm_button_3_2.hide()


    def handle_data_1(self):
        self.get_vehicle_widget.vehicle_list.clear()

        repair_days_input = self.input_area_0.text()
        try:
            repair_days = int(repair_days_input)
            if repair_days <= 0:
                self.comment_label_0.setText("Błąd, liczba dni musi być większa od 0")
                self.input_area_0.clear()
                return
            self.repair_days = repair_days
        except ValueError:
            self.comment_label_0.setText("Błąd, Podaj prawidłową liczbę dni naprawy")
            self.input_area_0.clear()
            return

        repair_rates_input = self.input_area_2.text()
        try:
            repair_rates = int(repair_rates_input)
            if repair_rates <= 0:
                self.comment_label_2.setText("Błąd, liczba dni musi być większa od 0")
                self.input_area_0.clear()
                return
            self.repair_rates = repair_rates
        except ValueError:
            self.comment_label_2.setText("Błąd, Podaj prawidłwe koszt jednostkowy naprawy")
            self.input_area_0.clear()
            return

        index = self.combo_area_1.currentIndex()
        self.work_user = self.combo_area_1.itemData(index)
        work_user_str = f"Wybrano: {self.work_user.first_name} {self.work_user.last_name}"
        self.total_cost =  repair_rates * repair_days
        item = f"Wybrano: {self.vehicle.brand} {self.vehicle.vehicle_model}  [{self.vehicle.individual_id}]"
        self.description = self.input_area_3.text()


        for text in [item, work_user_str, self.description, f"Liczba dni w naprawie: {repair_days}",
                    f"Całkowity koszt naprawy: {self.total_cost} zł"]:
            self.get_vehicle_widget.vehicle_list.addItem(text)
            self.get_vehicle_widget.adjust_list_height()

        today = date.today()
        self.planned_return_date = date.today() + timedelta(days=repair_days)
        broken_rent = self.session.query(RentalHistory).filter(
            RentalHistory.vehicle_id == self.vehicle.id,
            func.date(RentalHistory.start_date) <= self.planned_return_date,
            func.date(RentalHistory.planned_return_date) >= today
        ).first()

        if not broken_rent:

            self.mark_as_repair(self.session)

        self.get_vehicle_widget.vehicle_list.addItem("PYRAŻKA !!!")

    def mark_as_repair(self, session):
        self.container_hbox0.hide()
        self.container_hbox1.hide()
        self.container_hbox2.hide()
        self.container_hbox3.hide()

        repair_id = generate_repair_id(self.session)

        # Generowanie naprawy
        repair = RepairHistory(
            repair_id=repair_id,
            vehicle_id=self.vehicle.id,
            mechanic_id=self.work_user.id,
            start_date=date.today(),
            planned_return_date=self.planned_return_date,
            cost=self.total_cost,
            description=self.description)
        self.session.add(repair)

        # Aktualizacja pojazdu
        self.vehicle.is_available = False
        self.vehicle.borrower_id = self.work_user.id
        self.vehicle.return_date = self.planned_return_date

        session.commit()

        final_text = (
            f"\nPojazd: {self.vehicle.brand} {self.vehicle.vehicle_model} {self.vehicle.individual_id}\n"
            f"\nprzekazany do warsztatu: {self.work_user.first_name} {self.work_user.last_name} do dnia {self.planned_return_date}."
        )
        self.get_vehicle_widget.vehicle_list.clear()
        self.get_vehicle_widget.vehicle_list.addItem(final_text)
        self.get_vehicle_widget.vehicle_list.adjustSize()
        return True



















if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RepairVehicleWidget()
    main_window.showMaximized()
    sys.exit(app.exec())
