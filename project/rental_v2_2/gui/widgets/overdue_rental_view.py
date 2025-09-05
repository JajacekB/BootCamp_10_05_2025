import datetime
import platform
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QListWidget, QPushButton, QMessageBox, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal, QTimer, QDate

from gui.windows.calendar_combo_widget import CalendarCombo


class OverdueRentalView(QWidget):

    handle_get_overdue = Signal()
    handle_overdue_tasks_details = Signal(object)
    handle_overdue_update_db = Signal(object, QDate)

    def __init__(self, role):
        super().__init__()

        self.role = role
        self.overdue_tasks_dict = {}
        self.overdue_tasks_list = []

        self.setWindowTitle("Przeterminowane zwroty")

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
        QTimer.singleShot(0, lambda: self._get_overdue_vehicle_tasks())


    def _build_ui(self):
        self.main_layout = QVBoxLayout()

        self.title_label = QLabel(">>> Przeterminowane zwroty <<<")
        self.title_label.setStyleSheet("font-size: 26px; color: #A9C1D9; ")
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
        self.rentals_list.itemClicked.connect(self._on_overdue_tasks_details)

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
            "background-color: darkgreen;"
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

    def _get_overdue_vehicle_tasks(self):
        self.handle_get_overdue.emit()

    def show_no_overdue(self):
        self.rentals_list.clear()
        QMessageBox.information(
            self,
            "Brak zaległości",
            "Brak zaległości.\nPonowne sprawdzenie jutro."
        )
        self.title_label.hide()
        self.rentals_list.hide()
        self._hide_widget()

    def overdue_action(self, overdues):
        self.rentals_list.clear()
        self.title_label.show()
        self.rentals_list.show()

        for data in overdues:
            text = (
                f"|{data['id_number']:>7} "
                f"|{data['brand']:>15} "
                f"|{data['model']:>15} "
                f"|{data['vehicle_type']:>9} "
                f"|{data['start_date'].strftime('%d-%m-%Y'):>11} → "
                f"{data['end_date'].strftime('%d-%m-%Y'):<11} "
                f"|{data['cost']:>11} zł |"
            )
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, data["obj"])
            self.rentals_list.addItem(item)

        self.adjust_list_height()


    def _on_overdue_tasks_details(self, item):
        print(f"{item=}")

        obj = item.data(Qt.UserRole)
        self.handle_overdue_tasks_details.emit(obj)

    def show_overdue_items_detail(self, overdue_text):

        self.overdue_rental_detail.clear()
        self.overdue_rental_detail.setText(overdue_text)

        for widget in (self.overdue_rental_detail, self.cancel_button, self.finish_button):
            widget.show()

    def overdue_update_database(self, item):

        actual_return_date_input = self.calendar_input.get_date()

        for item in self.rentals_list.selectedItems():
            task = item.data(Qt.UserRole)

        self.handle_overdue_update_db.emit(task, actual_return_date_input)

    def summary_update_repair(self, success, msg):

        if success:
            QMessageBox.information(
                self,
                "Sukces, pojazd wrócił z naprawy",
                f"{msg}"
            )
        else:
            QMessageBox.warning(
                self,
                "Błąd",
                f"{msg}"
            )

        self._hide_widget()
        self._get_overdue_vehicle_tasks()

    def summary_rental(self, summary_text):

        QMessageBox.information(
            self,
            "Koniec najmu",
            f"{summary_text}"
        )
        self._hide_widget()
        self._get_overdue_vehicle_tasks()

    def overdue_finish(self):
        for widget in (self.calendar_comment_label, self.calendar_input, self.date_approve):
            widget.show()

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