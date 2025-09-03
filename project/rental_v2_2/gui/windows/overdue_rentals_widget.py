import sys, platform

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox
    )
from PySide6.QtCore import Qt
from datetime import date

from models.repair_history import RepairHistory
from models.vehicle import Vehicle



from gui.windows.calendar_combo_widget import CalendarCombo
from services.rental_costs import recalculate_cost
from services.database_update import update_database
from models.user import User
from models.rental_history import RentalHistory
# from models.vehicle import Vehicle, Car, Scooter, Bike
from database.base import SessionLocal

class OverdueRentalsWidget(QWidget):
    def __init__(self, session = None, user = None):
        super().__init__()

        self.session = session or SessionLocal()
        self.user = user

        self.setWindowTitle("Zwroty")
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e; 
                color: #eee; 
                font-size: 16px;
            }
            QPushButton {
                background-color: #555;
                border-radius: 6px;
                padding: 5px;
            }
            QLineEdit {
                font-size: 14px;
            }
        """)
        self._build_ui()
        self.overdue_vehicle_rentals()

    def _build_ui(self):
        self.main_layout = QVBoxLayout()

        self.title_label = QLabel(">>> Przeterminowane zwroty <<<")
        self.title_label.setStyleSheet("font-size: 26px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.rentals_list = QListWidget()
        font = self.rentals_list.font()
        system = platform.system()

        if system == "Windows":
            font.setFamily("Consolas")
        elif system == "Darwin":  # macOS
            font.setFamily("Menlo")
        else:  # Linux i inne
            font.setFamily("DejaVu Sans Mono")

        self.rentals_list.setFont(font)
        self.rentals_list.addItem("")
        self.adjust_list_height()
        self.main_layout.addWidget(self.rentals_list)
        self.rentals_list.itemClicked.connect(self.overdue_rental_details)

        self.overdue_rental_detail = QLabel()
        self.overdue_rental_detail.hide()
        self.overdue_rental_detail.setWordWrap(True)
        self.main_layout.addWidget(self.overdue_rental_detail, alignment=Qt.AlignLeft)


        hbox1 = QHBoxLayout()

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.hide()
        self.cancel_button.setStyleSheet(
            "background-color: red;"
            " font-size: 20px; color: white;"
            )
        self.cancel_button.setFixedSize(150, 45)
        # self.cancel_button.clicked.connect(self.cancel_rentals)
        hbox1.addWidget(self.cancel_button)

        self.finish_button = QPushButton("Tak")
        self.finish_button.hide()
        self.finish_button.setStyleSheet(
            "background-color: green;"
            " font-size: 20px; color: white;"
            )
        self.finish_button.setFixedSize(150, 45)
        self.finish_button.clicked.connect(self.overdue_finish)
        hbox1.addWidget(self.finish_button)

        hbox1.addStretch()
        self.main_layout.addLayout(hbox1)


        hbox2 = QHBoxLayout()

        self.calendar_comment_label = QLabel("Podaj rzeczywistą datę zwrotu: ")
        self.calendar_comment_label.hide()
        hbox2.addWidget(self.calendar_comment_label)

        self.calendar_input = CalendarCombo()
        self.calendar_input.hide()
        hbox2.addWidget(self.calendar_input)

        self.date_approve = QPushButton("Zatwierdź datę")
        self.date_approve.hide()
        self.date_approve.setStyleSheet(
            "background-color: grey;"
            " font-size: 20px; color: white;"
            )
        self.date_approve.setFixedSize(150, 45)
        self.date_approve.clicked.connect(self.overdue_update_database)
        hbox2.addWidget(self.date_approve)

        hbox2.addStretch()
        self.main_layout.addLayout(hbox2)

        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


    def overdue_update_database(self, item):
        actual_return_date_input = self.calendar_input.get_date()
        actual_return_date = actual_return_date_input.toPython()

        for item in self.rentals_list.selectedItems():
            obj = item.data(Qt.UserRole)

        if isinstance(obj, RepairHistory):
            obj.actual_return_date = actual_return_date
            obj.vehicle.is_available = True
            obj.vehicle.borrower_id = None
            obj.vehicle.return_date = None
            self.session.commit()

            QMessageBox.information(
                self,
                "Sukces",
                "Pojazd wrócił z naprawy."
            )

        elif isinstance(obj, RentalHistory):
            total_cost, extra_fee, summary_text = recalculate_cost(
                self.session,
                self.user,
                obj.vehicle,
                actual_return_date,
                obj.reservation_id
            )

            update_database(
                self.session,
                obj.vehicle,
                actual_return_date,
                total_cost,
                extra_fee,
                obj.reservation_id
            )

            QMessageBox.information(
                self,
                "Sukces, pojazd został zwrócony",
                f"{summary_text}"
            )

        # 🚀 Zresetuj GUI PRZED ponownym sprawdzeniem
        self._hide_widget() # <--- kluczowe
        self.overdue_vehicle_rentals()


    def overdues_action(self):
        self.rentals_list.clear()

        for obj in self.overdues:
            if isinstance(obj, RentalHistory):
                end_date = obj.actual_return_date or obj.planned_return_date
                id_number = obj.reservation_id
                cost = obj.total_cost
            elif isinstance(obj, RepairHistory):
                end_date = obj.actual_return_date or obj.planned_return_date
                id_number = obj.repair_id
                cost = obj.cost
            else:
                end_date = None
                id_number = None
                cost = None
            text = (
                f"|{id_number:>7} "
                f"|{obj.vehicle.brand:>15} "
                f"|{obj.vehicle.vehicle_model:>15} "
                f"|{getattr(obj.vehicle, 'type', ''):>9} "
                f"|{obj.start_date.strftime('%d-%m-%Y'):>11} → "
                f"{end_date.strftime('%d-%m-%Y'):<11} "
                f"|{cost:>11} zł |"
            )

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, obj)
            self.rentals_list.addItem(item)

        self.adjust_list_height()

    def overdue_rental_details(self, item):
        self.overdue_rental_detail.clear()

        obj = item.data(Qt.UserRole)

        id_number = getattr(obj, 'reservation_id', None) if isinstance(obj, RentalHistory) else getattr(obj,
            'repair_id', None)
        cost = getattr(obj, 'total_cost', None) if isinstance(obj, RentalHistory) else getattr(obj, 'cost', None)

        id_user = getattr(obj, 'user_id', None) if isinstance(obj, RentalHistory) else getattr(obj, 'mechanic_id', None)

        self.user =  self.session.query(User).filter(User.id == id_user).first()

        overdues_text = (
            f"Czy chcesz zakończyć?\n\n"
            f"ID: {id_number}\n"
            f"Pojazd: {obj.vehicle.brand} {obj.vehicle.vehicle_model}\n"
            f"Wynajęty/w naprawie od: {obj.start_date.strftime('%d-%m-%Y')} "
            f"do: {obj.planned_return_date.strftime('%d-%m-%Y')}\n"
            f"Do zapłaty: {cost} zł\n"
            f"Wynajęty przez: {self.user.first_name} {self.user.last_name}."
        )

        self.overdue_rental_detail.setText(overdues_text)
        self.adjust_list_height()

        for widget in (self.overdue_rental_detail, self.cancel_button, self.finish_button):
            widget.show()

    def overdue_finish(self):
        for widget in (self.calendar_comment_label, self.calendar_input, self.date_approve):
            widget.show()

    def overdue_vehicle_rentals(self):
        today = date.today()

        # Pobierz zaległe wynajmy i naprawy
        rentals = (
            self.session.query(RentalHistory)
            .filter(RentalHistory.planned_return_date < today,
                    RentalHistory.actual_return_date == None)
            .all()
        )

        repairs = (
            self.session.query(RepairHistory)
            .filter(RepairHistory.planned_return_date < today,
                    RepairHistory.actual_return_date == None)
            .all()
        )

        self.overdues = rentals + repairs

        # Jeśli brak zaległości → czyść listę i pokaż komunikat
        if not self.overdues:
            self.rentals_list.clear()
            QMessageBox.information(
                self,
                "Brak zaległości",
                "Brak zaległości.\nPonowne sprawdzenie jutro."
            )
            self.title_label.hide()
            self.rentals_list.hide()
            self._hide_widget()

        else:
            self.overdues_action()

    def _hide_widget(self):
        self.overdue_rental_detail.clear()
        self.overdue_rental_detail.hide()
        self.cancel_button.hide()
        self.finish_button.hide()
        self.calendar_comment_label.hide()
        self.calendar_input.hide()
        self.date_approve.hide()
        self.rentals_list.clear()

    def adjust_list_height(self):
        if self.rentals_list.count() > 0:
            row_height = self.rentals_list.sizeHintForRow(0)
            spacing = self.rentals_list.spacing()
            min_rows = 5
            max_rows = 10
            rows = max(min(self.rentals_list.count(), max_rows), min_rows)
            total_height = row_height * rows + spacing * (rows - 1) + 4
            self.rentals_list.setFixedHeight(total_height)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_windows = OverdueRentalsWidget()
    main_windows.showMaximized()
    sys.exit(app.exec())