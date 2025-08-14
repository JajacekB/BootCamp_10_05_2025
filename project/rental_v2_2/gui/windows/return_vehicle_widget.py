import sys
import platform

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox
    )
from PySide6.QtCore import Qt


from gui.windows.calendar_combo_widget import CalendarCombo
from services.rental_costs import recalculate_cost
from services.database_update import update_database
from models.user import User
from models.rental_history import RentalHistory
# from models.vehicle import Vehicle, Car, Scooter, Bike
from database.base import SessionLocal


class ReturnVehicleWidget(QWidget):
    def __init__(self, session = None, user = None):
        super().__init__()

        self.session = session or SessionLocal()
        self.user = user
        # self.user = self.session.query(User).filter(User.login == "tester").first()

        self.setWindowTitle("Zwroty")

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

        self.main_layout = QVBoxLayout()

        self.title_label = QLabel("Historia wypożyczeń:")
        self.title_label.setStyleSheet("font-size: 26px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.rentals_combo_box = QComboBox()
        self.rentals_combo_box.addItems(["Wszystkie", "Historyczne", "Aktywne"])
        self.form_layout = QFormLayout()
        self.form_layout.addRow("Jakie wynajmy chcesz przeglądąć?", self.rentals_combo_box)
        self.main_layout.addLayout(self.form_layout)

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
        self.rentals_list.itemClicked.connect(self.show_rental_details)

        self.show_button = QPushButton("Pokaż")
        self.show_button.setStyleSheet(
            "background-color: green;"
            " font-size: 20px; color: white;"
            " border-radius: 8px; padding: 6px; "
        )
        self.show_button.setFixedSize(150, 45)
        self.main_layout.addWidget(self.show_button, alignment=Qt.AlignRight)
        self.show_button.clicked.connect(self.load_rentals)

        self.grid_layout = QGridLayout()
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.grid_layout)
        self.main_layout.addWidget(self.grid_widget)

        self.finish_rental_label = QLabel()
        self.finish_rental_label.hide()
        self.finish_rental_label.setWordWrap(True)
        self.grid_layout.addWidget(self.finish_rental_label, 0, 0, 1, 4)


        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.hide()
        self.cancel_button.setStyleSheet(
            "background-color: red;"
            " font-size: 20px; color: white;"
            " border-radius: 8px; padding: 6px; ")
        self.cancel_button.setFixedSize(150, 45)
        self.cancel_button.clicked.connect(self.cancel_rentals)
        self.grid_layout.addWidget(self.cancel_button, 1, 0, 1, 1, alignment=Qt.AlignLeft)

        self.finish_button = QPushButton("Tak")
        self.finish_button.hide()
        self.finish_button.setStyleSheet(
            "background-color: green;"
            " font-size: 20px; color: white;"
            " border-radius: 8px; padding: 6px; ")
        self.finish_button.setFixedSize(150, 45)
        self.finish_button.clicked.connect(self.finish_rentals)
        self.grid_layout.addWidget(self.finish_button, 1, 1, 1, 1, alignment=Qt.AlignLeft)

        self.calendar_input = CalendarCombo()
        self.calendar_input.hide()
        self.grid_layout.addWidget(self.calendar_input, 2, 1, 1, 1, alignment=Qt.AlignLeft)
        self.calendar_comment_label = QLabel("Podaj rzeczywistą datę zwrotu: ")
        self.calendar_comment_label.hide()
        self.grid_layout.addWidget(self.calendar_comment_label, 2, 0, 1, 1, alignment=Qt.AlignRight)
        # self.calendar_input.emit_date_changed()

        self.final_cost_label = QLabel()
        self.final_cost_label.setWordWrap(True)
        self.grid_layout.addWidget(self.final_cost_label, 2, 2, 2, 2, alignment=Qt.AlignLeft)

        self.take_date_button = QPushButton("Potwierdź datę")
        self.take_date_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 20px; color: white;"
            " border-radius: 8px; padding: 6px; ")
        self.take_date_button.hide()
        self.grid_layout.addWidget(self.take_date_button, 3, 1, 1, 1, alignment=Qt.AlignLeft)
        self.take_date_button.setFixedSize(150, 45)
        self.take_date_button.clicked.connect(self.end_rental)

        self.confirm_end_button = QPushButton("Potwierdź koniec najmu")
        self.confirm_end_button.hide()
        self.confirm_end_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 20px; color: white;"
            " border-radius: 8px; padding: 6px; ")
        self.confirm_end_button.setFixedSize(250, 45)
        self.confirm_end_button.clicked.connect(self.finalize_rental)
        self.grid_layout.addWidget(self.confirm_end_button, 4, 2, 1, 1, alignment=Qt.AlignLeft)

        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def load_rentals(self):
        self.rentals_list.clear()

        for rental in self.get_rentals_from_db():
            if rental is None:
                separator_item = QListWidgetItem("")
                separator_item.setFlags(Qt.NoItemFlags)
                self.rentals_list.addItem(separator_item)
                continue

            return_date = rental.actual_return_date or rental.planned_return_date
            text = (
                f"|{rental.reservation_id:>7} "
                f"|{rental.vehicle.brand:>15} "
                f"|{rental.vehicle.vehicle_model:>15} "
                f"|{rental.vehicle.type:>9} "
                f"|{rental.start_date.strftime('%d-%m-%Y'):>11} → "
                f"{return_date.strftime('%d-%m-%Y'):<11}"
                f"|{rental.total_cost:>11} zł |"
            )

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, rental)

            if rental.actual_return_date is not None:
                item.setFlags(Qt.NoItemFlags)
                item.setForeground(Qt.gray)
            else:
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

            self.rentals_list.addItem(item)

        self.adjust_list_height()

    def get_rentals_from_db(self):
        mode = self.rentals_combo_box.currentText()

        active_rentals = self.session.query(RentalHistory).filter(
            RentalHistory.user_id == self.user.id,
            RentalHistory.actual_return_date.is_(None)
        ).order_by(RentalHistory.planned_return_date).all()

        historical_rentals = self.session.query(RentalHistory).filter(
            RentalHistory.user_id == self.user.id,
            RentalHistory.actual_return_date.isnot(None)
        ).order_by(RentalHistory.planned_return_date.desc()).all()

        if mode == "Aktywne":
            return active_rentals
        elif mode == "Historyczne":
            return historical_rentals
        else:
            return active_rentals + [None] + historical_rentals

    def show_rental_details(self):
        item = self.rentals_list.currentItem()
        if not item:
            return

        rental = item.data(Qt.UserRole)
        if rental is None or rental.actual_return_date is not None:
            return

        self.finish_rental_label.show()
        self.cancel_button.show()
        self.finish_button.show()

        rental_text = (
            f"Czy chcesz zakończyć ten wynajem?\n\n"
            f"ID: {rental.reservation_id}\n"
            f"Pojazd: {rental.vehicle.brand} {rental.vehicle.vehicle_model}\n"
            f"Wynajęty od: {rental.start_date.strftime('%d-%m-%Y')} "
            f"do: {(rental.actual_return_date or rental.planned_return_date).strftime('%d-%m-%Y')}\n"
            f"Do zapłaty: {rental.total_cost} zł"
        )
        self.finish_rental_label.setText(rental_text)

    def finish_rentals(self):

        self.calendar_comment_label.show()
        self.calendar_input.show()
        self.take_date_button.show()

    def end_rental(self):

        self.final_cost_label.clear()

        actual_return_date_input = self.calendar_input.get_date()
        actual_return_date_input_data = actual_return_date_input.toPython()

        item = self.rentals_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Uwaga", "Nie wybrano wynajmu!")
            return
        rental = item.data(Qt.UserRole)

        total_cost, extra_fee, summary_text = recalculate_cost(
            self.session, self.user, rental.vehicle, actual_return_date_input_data, rental.reservation_id
        )
        self.temp_actual_return_date = actual_return_date_input_data
        self.temp_total_cost = total_cost
        self.temp_extra_fee = extra_fee

        self.final_cost_label.setText(summary_text)
        self.final_cost_label.show()
        self.confirm_end_button.show()

    def finalize_rental(self):
        try:
            item = self.rentals_list.currentItem()
            rental = item.data(Qt.UserRole) if item else None
            if not rental or rental.actual_return_date is not None:
                return

            update_database(
                self.session,
                rental.vehicle,
                self.temp_actual_return_date,
                self.temp_total_cost,
                self.temp_extra_fee,
                rental.reservation_id
            )

            QMessageBox.information(self, "Sukces", "Zwrot został pomyślnie zarejestrowany.")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Błąd",
                f"Wystąpił błąd podczas finalizowania zwrotu:\n{str(e)}"
            )

    def cancel_rentals(self):

        self.finish_rental_label.clear()
        self.cancel_button.hide()
        self.finish_button.hide()
        self.calendar_input.hide()
        self.calendar_comment_label.hide()
        self.final_cost_label.clear()
        self.take_date_button.hide()
        self.confirm_end_button.hide()

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
    main_window = ReturnVehicleWidget()
    main_window.showMaximized()
    sys.exit(app.exec())
