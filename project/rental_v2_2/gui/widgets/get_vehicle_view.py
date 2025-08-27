# gui.widgets.get_vehicle_view.py
import sys
import platform
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox,
        QApplication, QListWidget, QListWidgetItem, QMessageBox, QGroupBox, QHBoxLayout
    )
from PySide6.QtCore import Qt, Signal

from models.vehicle import Vehicle


class GetVehicleView(QWidget):

    request_vehicle_list = Signal(str, str, str)
    vehicle_selected = Signal(object)

    def __init__(self, role = "client"):
        super().__init__()
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

    def _build_ui(self):

        self.main_layout = QVBoxLayout()

        self.title_label = QLabel("Przegląd pojazdów w wypozyczalni:")
        self.title_label.setStyleSheet("font-size: 28px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.status_combo_box = QComboBox()
        self.status_combo_box.addItems(["Wszystkie", "Dostępne", "Niedostępne"])

        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(["Wszystkie", "Samochody", "Skutery", "Rowery"])

        self.filters_group = QGroupBox("Filtry wyszukiwania")
        self.form_layout = QFormLayout()

        if self.role in ("admin", "seller"):
            self.form_layout.addRow("Wybierz czy chcesz przeglądać pojazdy dostępne:", self.status_combo_box)

        self.form_layout.addRow("Jaki rodzaj pojazdów chcesz przeglądać:", self.type_combo_box)

        self.search_button = QPushButton("Pokaż")
        self.search_button.setStyleSheet(
            "background-color: green;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")
        self.search_button.setFixedSize(120, 35)
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
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


    def on_request_vehicle_list(self):

        if self.role in ("admin", "seller"):
            status = self.status_combo_box.currentText()
        else:
            status = "Dostępne"
        v_type = self.type_combo_box.currentText()
        print(f"[RepairView] Filtry GUI: status={status}, v_type={v_type}")
        self.request_vehicle_list.emit(status, v_type, self.role)

    def handle_item_clicked(self, item: QListWidgetItem):
        data = item.data(Qt.UserRole)

        if isinstance(data, list) and all(isinstance(v, Vehicle) for v in data):
            self.list_widget.clear()
            for vehicle in data:
                v_item = QListWidgetItem(f"{vehicle.brand} {vehicle.vehicle_model} ({vehicle.individual_id})")
                v_item.setData(Qt.UserRole, vehicle)
                self.list_widget.addItem(v_item)
        elif isinstance(data, Vehicle):
            self.vehicle_selected.emit(data)

    def show_vehicle_list(self, vehicles_grouped):
        self.list_widget.clear()
        for (brand, model, cash_per_day), group in vehicles_grouped.items():
            count = len(group)
            display_text = f"{brand} {model} – {cash_per_day:.2f} zł/dzień - ({count} szt.)"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, group)
            self.list_widget.addItem(item)
        self.adjust_list_height()

    def show_vehicle_list_readonly(self, vehicles_grouped):
        self.list_widget.clear()

        # Odłącz wszystkie połączenia itemClicked
        try:
            self.list_widget.itemClicked.disconnect()
        except TypeError:
            pass  # jeśli nie było połączenia, ignorujemy

        # Wyłącz zaznaczanie
        self.list_widget.setSelectionMode(QListWidget.NoSelection)

        for (brand, model, cash_per_day), group in vehicles_grouped.items():
            display_text = f"{brand} {model} – {cash_per_day:.2f} zł/dzień"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, group)
            item.setFlags(Qt.NoItemFlags)
            self.list_widget.addItem(item)
        self.adjust_list_height()

    # def show_vehicle_list_readonly(self, vehicles_grouped):
    #     self.list_widget.clear()
    #     for (brand, model, cash_per_day), group in vehicles_grouped.items():
    #         display_text = f"{brand} {model} – {cash_per_day:.2f} zł/dzień"
    #         item = QListWidgetItem(display_text)
    #         item.setData(Qt.UserRole, group)
    #         item.setFlags(Qt.NoItemFlags)
    #         self.list_widget.addItem(item)
    #     self.adjust_list_height()

    def show_vehicle_history(self, vehicle, rentals=None, repairs=None):
        self.list_widget.clear()
        vehicle_text = f"Wybrano: ID[{vehicle.vehicle_id}] {vehicle.brand} {vehicle.vehicle_model} nr:{vehicle.individual_id}"
        self.list_widget.addItem(vehicle_text)

        if not rentals:
            error_text = "Brak historii wyporzyczeń"
            self.list_widget.addItem(error_text)
        else:
            for r in rentals:
                rental_text = (f" ID:[{r.id}] Nr rezerwacji: {r.reservation_id} "
                    f"Klient: {r.user.first_name} {r.user.last_name} "
                    f"w termine od {r.start_date} do {r.planned_return_date}.")
                self.list_widget.addItem(rental_text)

        if not repairs:
            error_text = "Brak historii napraw"
            self.list_widget.addItem(error_text)
        else:
            for n in repairs:
                rental_text = (f" ID:[{n.id}] Nr naprawy: {n.repair_id} "
                    f"Warsztat: {n.mechanic.first_name} {n.mechanic.last_name} "
                    f"w termine od {n.start_date} do {n.planned_return_date}.")
                self.list_widget.addItem(rental_text)

        self.adjust_list_height()

        """

        :param rentals:
        :param repairs:
        :return:
        """






    def show_errors(self, messages: list[str]):
        self.list_widget.clear()
        for msg in messages:
            self.list_widget.addItem(f"🚫 {msg}")
        self.adjust_list_height()

    def adjust_list_height(self):
        count = self.list_widget.count()
        row_height = self.list_widget.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.list_widget.frameWidth()
        new_height = min(17, max(5, count)) * row_height + frame
        self.list_widget.setMinimumHeight(new_height)
        self.list_widget.setMaximumHeight(new_height)