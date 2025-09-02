from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QListWidgetItem,
    QGroupBox, QFormLayout, QHBoxLayout, QListWidget, QMessageBox
)
from PySide6.QtCore import Qt, Signal
import platform

from models.vehicle import Vehicle


class DeleteVehicleView(QWidget):

    request_vehicle_list = Signal(str)
    request_delete_vehicle = Signal(object)

    def __init__(self):
        super().__init__()

        self.vehicle_to_delete = None

        self.setWindowTitle("Usuń pojazd")

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

        self.title_label = QLabel("Przegląd pojazdów w wypozyczalni:")
        self.title_label.setStyleSheet("font-size: 28px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(["Wszystkie", "Samochody", "Skutery", "Rowery"])

        self.filters_group = QGroupBox("Filtry wyszukiwania")
        self.form_layout = QFormLayout()

        self.form_layout.addRow("Jaki rodzaj pojazdów chcesz przeglądać:", self.type_combo_box)

        self.search_button = QPushButton("Pokaż")
        self.search_button.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")
        self.search_button.setFixedSize(210, 35)
        self.search_button.clicked.connect(self.on_request_vehicle_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addStretch()
        self.form_layout.addRow("", button_layout)

        filters_layout = QVBoxLayout()
        filters_layout.addLayout(self.form_layout)

        self.filters_group.setLayout(filters_layout)
        self.main_layout.addWidget(self.filters_group)

        self.list_widget = QListWidget()
        font = self.list_widget.font()
        system = platform.system()

        if system == "Windows":
            font.setFamily("Consolas")
        elif system == "Darwin":  # macOS
            font.setFamily("Menlo")
        else:  # Linux i inne
            font.setFamily("DejaVu Sans Mono")

        self.list_widget.setFont(font)
        self.adjust_list_height()
        self.list_widget.itemClicked.connect(self.handle_item_clicked)

        self.main_layout.addWidget(self.list_widget)

        self.confirmation_widget = QWidget()
        self.confirmation_layout = QVBoxLayout(self.confirmation_widget)

        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.confirmation_layout.addWidget(self.info_label)

        buttons_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.setStyleSheet(
            "background-color: brown;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")
        self.cancel_button.setFixedSize(210, 35)

        self.confirm_button = QPushButton("Potwierdź usunięcie")
        self.confirm_button.setStyleSheet(
            "background-color: darkgreen;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")
        self.confirm_button.setFixedSize(210, 35)

        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.confirm_button)

        self.confirmation_layout.addLayout(buttons_layout)

        self.main_layout.addWidget(self.confirmation_widget)
        self.confirmation_widget.setVisible(False)

        self.confirm_button.clicked.connect(self._on_click_confirm_delete)
        self.cancel_button.clicked.connect(self._cancel_delete)



        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def on_request_vehicle_list(self):

        v_type = self.type_combo_box.currentText()
        print(f"[RepairView] Filtry GUI: v_type={v_type}")
        self.request_vehicle_list.emit(v_type)

    def show_vehicle_list(self, vehicles_grouped):
        self.list_widget.clear()
        for (brand, model, cash_per_day), group in vehicles_grouped.items():
            count = len(group)
            daly_rate = f"{cash_per_day:.2f}"
            display_text = (
                f"{brand:<13} {model:<13} – "
                f"{daly_rate:>7} zł/dzień - "
                f"[{count:>7} szt.]"
            )
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, group)
            self.list_widget.addItem(item)
        self.adjust_list_height()

    def show_group_members(self, group):
        self.list_widget.clear()

        for v in group:
            display_text = (
                f"🔹 {v.brand} {v.vehicle_model}  -  "
                f"{v.cash_per_day:.2f} zł/dzień,  [{v.individual_id}]"
            )
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, v)
            # item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.list_widget.addItem(item)
            self.adjust_list_height()

    def handle_item_clicked(self, item):
        data = item.data(Qt.UserRole)

        if data == "return":
            self.on_request_vehicle_list()  # wróć do widoku grup
            return
        if isinstance(data, list):
            self.show_group_members(data)
            self.list_widget.itemClicked.disconnect()
            self.list_widget.itemClicked.connect(self.handle_single_vehicle_click)
        else:
            self.handle_single_vehicle_click(item)

    def handle_single_vehicle_click(self, item):
        vehicle = item.data(Qt.UserRole)

        if isinstance(vehicle, list):
            self.show_group_members(vehicle)
            self.list_widget.itemClicked.disconnect()
            self.list_widget.itemClicked.connect(self.handle_single_vehicle_click)
            return

        if not vehicle:
            QMessageBox.information(self, "Informacja", item.text())
            return

        self.list_widget.setEnabled(False)
        self.confirmation_widget.setVisible(True)

        self.info_label.setText(
            f"Czy na pewno chcesz usunąć ten pojazd?\n\n{vehicle.get_display_info()}"
        )

        self.vehicle_to_delete = vehicle

    def _on_click_confirm_delete(self):
        if not self.vehicle_to_delete:
            return
        self.request_delete_vehicle.emit(self.vehicle_to_delete)

    def success_deactivate(self, text):
        QMessageBox.information(self,"Sukces", text)
        self._reset_after_delete()

    def error_deactivate(self, text):
        QMessageBox.critical(self,"Błąd zapisu bazy danych", text)
        self._reset_after_delete()

    def _cancel_delete(self):
        self._reset_after_delete()

    def _reset_after_delete(self):
        self.confirmation_widget.setVisible(False)
        self.list_widget.setEnabled(True)
        self.vehicle_to_delete = None
        self.on_request_vehicle_list()


    def adjust_list_height(self):
        count = self.list_widget.count()
        row_height = self.list_widget.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.list_widget.frameWidth()
        new_height = min(17, max(5, count)) * row_height + frame
        self.list_widget.setMinimumHeight(new_height)
        self.list_widget.setMaximumHeight(new_height)