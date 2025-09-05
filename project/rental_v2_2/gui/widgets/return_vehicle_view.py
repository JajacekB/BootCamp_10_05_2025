# gui.widgets.return_vehicle_view.py
import platform
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox,
        QListWidget, QListWidgetItem, QMessageBox, QGroupBox, QHBoxLayout, QGridLayout
    )
from PySide6.QtCore import Qt, Signal

from gui.windows.calendar_combo_widget import CalendarCombo


class ReturnVehicleView(QWidget):

    handle_rentals_list = Signal(str)
    handle_rental_detail = Signal(object)
    handle_end_rental = Signal(object, object, str)
    handle_finalize_rental = Signal(object)


    def __init__(self, role = "client"):
        super().__init__()
        self.controller = None
        self.role = role

        self.setWindowTitle("Pojazdy")

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

    def set_controller(self, controller):
        self.controller = controller
        self.controller.operation_success.connect(self.finalize_success)
        self.controller.operation_error.connect(self.finalize_error)

    def _build_ui(self):
        self.main_layout = QVBoxLayout()

        self.title_label = QLabel("=== Historia wypożyczeń ===")
        self.title_label.setStyleSheet("font-size: 26px; color: #A9C1D9; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.filters_group = QGroupBox("Filtry wyszukiwania")
        self.form_layout = QFormLayout()

        self.rentals_combo_box = QComboBox()
        self.rentals_combo_box.addItems(["Wszystkie", "Historyczne", "Aktywne"])
        self.form_layout = QFormLayout()
        self.form_layout.addRow("Jakie wynajmy chcesz przeglądąć?", self.rentals_combo_box)

        self.show_button = QPushButton("Pokaż")
        self.show_button.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 20px; color: white;"
            " border-radius: 8px; padding: 4px; "
        )
        self.show_button.setFixedSize(150, 40)
        self.show_button.clicked.connect(self.on_click_rental_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.show_button)
        button_layout.addStretch()
        self.form_layout.addRow("", button_layout)

        filters_layout = QVBoxLayout()
        filters_layout.addLayout(self.form_layout)

        self.filters_group.setLayout(filters_layout)
        self.main_layout.addWidget(self.filters_group)

        self.rentals_list = QListWidget()
        font = self.rentals_list.font()
        system = platform.system()
        if system == "Windows":
            font.setFamily("Consolas")
        elif system == "Darwin":
            font.setFamily("Menlo")
        else:
            font.setFamily("DejaVu Sans Mono")
        self.rentals_list.setFont(font)
        self.rentals_list.addItem("")
        self.adjust_list_height()
        self.main_layout.addWidget(self.rentals_list)
        self.rentals_list.itemClicked.connect(self.on_click_rental_details)



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
            "background-color: brown;"
            " font-size: 20px; color: white;"
            " border-radius: 8px; padding: 4px; ")
        self.cancel_button.setFixedSize(150, 40)
        self.cancel_button.clicked.connect(self.cancel_rentals)
        self.grid_layout.addWidget(self.cancel_button, 1, 0, 1, 1, alignment=Qt.AlignLeft)

        self.finish_button = QPushButton("Tak")
        self.finish_button.hide()
        self.finish_button.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 20px; color: white;"
            " border-radius: 8px; padding: 4px; ")
        self.finish_button.setFixedSize(150, 40)
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
            " border-radius: 8px; padding: 4px; ")
        self.take_date_button.hide()
        self.grid_layout.addWidget(self.take_date_button, 3, 1, 1, 1, alignment=Qt.AlignLeft)
        self.take_date_button.setFixedSize(150, 40)
        self.take_date_button.clicked.connect(self.on_click_end_rental)

        self.confirm_end_button = QPushButton("Potwierdź koniec najmu")
        self.confirm_end_button.hide()
        self.confirm_end_button.setStyleSheet(
            "background-color: grey;"
            " font-size: 20px; color: white;"
            " border-radius: 8px; padding: 4px; ")
        self.confirm_end_button.setFixedSize(250, 40)
        self.confirm_end_button.clicked.connect(self.on_click_finalize_rental)
        self.grid_layout.addWidget(self.confirm_end_button, 4, 2, 1, 1, alignment=Qt.AlignLeft)

        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def on_click_rental_list(self):
        mode = self.rentals_combo_box.currentText()
        self.handle_rentals_list.emit(mode)

    def on_click_rental_details(self):
        item = self.rentals_list.currentItem()
        if not item:
            return
        rental = item.data(Qt.UserRole)
        self.handle_rental_detail.emit(rental)

    def on_click_end_rental(self):
        actual_return_date_input = self.calendar_input.get_date()
        actual_return_date_input_data = actual_return_date_input.toPython()

        item = self.rentals_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Uwaga", "Nie wybrano wynajmu!")
            return
        rental = item.data(Qt.UserRole)
        self.handle_end_rental.emit(rental.vehicle, actual_return_date_input_data, rental.reservation_id)

    def on_click_finalize_rental(self):
        item = self.rentals_list.currentItem()
        rental = item.data(Qt.UserRole) if item else None
        if not rental or rental.actual_return_date is not None:
            return
        self.handle_finalize_rental.emit(rental)

    def load_rentals(self, rentals):
        self.rentals_list.clear()

        for rental in rentals:
            if rental is None:
                separator_item = QListWidgetItem("")
                separator_item.setFlags(Qt.NoItemFlags)
                self.rentals_list.addItem(separator_item)
                continue

            return_date = rental.actual_return_date or rental.planned_return_date
            text = (
                f"|{rental.reservation_id:>7} "
                f"|{rental.vehicle.brand:>11} "
                f"|{rental.vehicle.vehicle_model:>13} "
                f"|{rental.vehicle.type:>7} "
                f"|{rental.start_date.strftime('%d-%m-%Y'):>11} → "
                f"{return_date.strftime('%d-%m-%Y'):<11}"
                f"|{rental.total_cost:>7} zł |"
            )
            print(rental)

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, rental)

            if rental.actual_return_date is not None:
                item.setFlags(Qt.NoItemFlags)
                item.setForeground(Qt.gray)
            else:
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

            self.rentals_list.addItem(item)
        self.adjust_list_height()

    def show_rental_details(self, details):

        if details is None:
            return

        rental_text = (
            f"Czy chcesz zakończyć ten wynajem?\n\n"
            f"ID: {details['reservation_id']}\n"
            f"Pojazd: {details['vehicle']}\n"
            f"Wynajęty od: {details['start_date'].strftime('%d-%m-%Y')} "
            f"do: {details['end_date'].strftime('%d-%m-%Y')}\n"
            f"Do zapłaty: {details['total_cost']} zł"
        )

        self.finish_rental_label.setText(rental_text)
        self.finish_rental_label.show()
        self.cancel_button.show()
        self.finish_button.show()

    def finish_rentals(self):

        self.calendar_comment_label.show()
        self.calendar_input.show()
        self.take_date_button.show()

    def end_rental(self, summary_text):

        self.final_cost_label.clear()

        self.final_cost_label.setText(summary_text)
        self.final_cost_label.show()
        self.confirm_end_button.show()

    def finalize_success(self, success_text):
        QMessageBox.information(
            self,
            "Sukces",
            success_text
        )
        self.cancel_rentals()

    def finalize_error(self, error_text):
        QMessageBox.critical(
            self,
            "Błąd",
            error_text
        )
        self.cancel_rentals()

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
