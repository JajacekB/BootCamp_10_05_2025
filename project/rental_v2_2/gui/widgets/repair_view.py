# repair_view.py
import platform
from collections import defaultdict
from datetime import date, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QLabel, QGroupBox,
    QComboBox, QListWidget, QLineEdit, QSizePolicy, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal, QTimer, QDate

from services.user_service import get_users_by_role
from models.vehicle import Vehicle
from services.vehicle_avability import get_unavailable_vehicle, get_available_vehicles


class RepairVehicleView(QWidget):
    request_vehicle_list = Signal(str, str)
    vehicle_selected = Signal(object)
    vehicle_id_entered = Signal(str)
    submit_repair_info = Signal(str, int, int, str, int)  # vehicle_id, dni, koszt/dzień, opis, workshop_index
    rental_choice_selected = Signal(str)  # Kontynuuje/Kończy wynajem
    click_summary_button = Signal() # Jeszcze nie wiem co będzie robił
    replacement_choice_selected = Signal(str)  # Droższy/Tańszy/Anuluje
    finalize_repair_signal = Signal()  # sygnał do finalizacji repair

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Naprawa pojazdu")
        self.setStyleSheet("""
            QWidget { background-color: #2e2e2e; color: #eee; font-size: 18px; }
            QPushButton { background-color: #555; border-radius: 5px; padding: 5px; }
            QLineEdit { font-size: 16px; }
        """)

        self._build_ui()

    def _build_ui(self):
        self.main_layout = QVBoxLayout()

        # --- Tytuł ---
        self.title_label = QLabel("Przegląd pojazdów w wypozyczalni:")
        self.title_label.setStyleSheet("font-size: 28px; color: white; ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # --- Comboboxy ---
        self.status_combo_box = QComboBox()
        self.status_combo_box.addItems(["Wszystkie", "Dostępne", "Niedostępne"])

        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(["Wszystkie", "Samochody", "Skutery", "Rowery"])

        # --- Grupa filtrów ---
        self.filters_group = QGroupBox("Filtry wyszukiwania")

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Wybierz czy chcesz przeglądać pojazdy dostępne:", self.status_combo_box)
        self.form_layout.addRow("Jaki rodzaj pojazdów chcesz przeglądać:", self.type_combo_box)

        # --- Przycisk Pokaż ---
        self.search_button = QPushButton("Pokaż")
        self.search_button.setStyleSheet(
            "background-color: green;"
            " font-size: 18px; color: white;"
            " border-radius: 8px; padding: 6px; ")
        self.search_button.setFixedSize(120, 35)
        self.search_button.clicked.connect(self.on_request_vehicle_list)

        # --- Poziomy layout na przycisk ---
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addStretch()
        self.form_layout.addRow("", button_layout)

        # --- Scalone w pionie: filtry + przycisk ---
        filters_layout = QVBoxLayout()
        filters_layout.addLayout(self.form_layout)

        self.filters_group.setLayout(filters_layout)
        self.main_layout.addWidget(self.filters_group)

        # Lista pojazdów
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

        # --- Pojazd po podanym vehicle_ID ---
        self.input_vehicle_id = QLineEdit()
        self.input_vehicle_id.setPlaceholderText("Podaj ID pojazdu")
        self.confirm_vehicle_button = QPushButton("Wybierz pojazd")
        self.confirm_vehicle_button.clicked.connect(self.on_confirm_vehicle)

        self.hbox_vehicle = QHBoxLayout()
        self.hbox_vehicle.addWidget(self.input_vehicle_id)
        self.hbox_vehicle.addWidget(self.confirm_vehicle_button)
        self.container_1 = QWidget()
        self.container_1.setLayout(self.hbox_vehicle)
        # self.container_1.hide()
        self.main_layout.addWidget(self.container_1)

        # --- Dane naprawy ---
        self.input_repair_days = QLineEdit()
        self.input_repair_days.setPlaceholderText("Liczba dni naprawy")
        self.input_repair_cost = QLineEdit()
        self.input_repair_cost.setPlaceholderText("Koszt naprawy / dzień")
        self.input_repair_desc = QLineEdit()
        self.input_repair_desc.setPlaceholderText("Opis naprawy")
        self.combo_workshop = QComboBox()

        self.submit_repair_button = QPushButton("Zatwierdź dane naprawy")
        self.submit_repair_button.clicked.connect(self.on_submit_repair)

        form_layout = QFormLayout()
        form_layout.addRow("Dni naprawy:", self.input_repair_days)
        form_layout.addRow("Koszt / dzień:", self.input_repair_cost)
        form_layout.addRow("Opis:", self.input_repair_desc)
        form_layout.addRow("Warsztat:", self.combo_workshop)
        form_layout.addRow("", self.submit_repair_button)

        self.container_2 = QWidget()
        self.container_2.setLayout(form_layout)
        self.container_2.hide()
        self.main_layout.addWidget(self.container_2)

        # --- Wybór kontynuacji wynajmu ---
        self.combo_rental_choice = QComboBox()
        self.combo_rental_choice.addItems(["Kontynuuje wynajem", "Kończy wynajem"])
        self.combo_rental_choice.hide()
        self.rental_choice_button = QPushButton("Zatwierdź wybór")
        self.rental_choice_button.hide()
        self.rental_choice_button.clicked.connect(self.on_rental_choice_clicked)

        hbox_rental = QHBoxLayout()
        hbox_rental.addWidget(self.combo_rental_choice)
        hbox_rental.addWidget(self.rental_choice_button)
        self.main_layout.addLayout(hbox_rental)

        self.summary_button = QPushButton("Zatwierdź pojazd")
        self.summary_button.hide()
        self.summary_button.clicked.connect(self.on_click_summary_button)
        self.main_layout.addWidget(self.summary_button)

        # --- Wybór pojazdu zastępczego ---
        self.combo_replacement_choice = QComboBox()
        self.combo_replacement_choice.addItems(["Droższy", "Tańszy", "Anuluje wynajem"])
        self.combo_replacement_choice.hide()
        self.replacement_choice_button = QPushButton("Zatwierdź pojazd zastępczy")
        self.replacement_choice_button.hide()
        self.replacement_choice_button.clicked.connect(self.on_replacement_choice_clicked)

        hbox_replacement = QHBoxLayout()
        hbox_replacement.addWidget(self.combo_replacement_choice)
        hbox_replacement.addWidget(self.replacement_choice_button)
        self.main_layout.addLayout(hbox_replacement)

        # --- Finalizacja ---
        self.finalize_button = QPushButton("Oddaj do naprawy")
        self.finalize_button.hide()
        self.finalize_button.clicked.connect(lambda: self.finalize_repair_signal.emit())
        self.main_layout.addWidget(self.finalize_button)

        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    # def _on_refresh_clicked(self):
    #     self.request_vehicle_list.emit()

    def update_vehicle_list(self, vehicles: list):
        """Aktualizacja listy pojazdów w widoku."""
        self.list_widget.clear()
        for v in vehicles:
            self.list_widget.addItem(str(v))

    def on_request_vehicle_list(self):
        """Emituj żądanie pobrania listy pojazdów."""
        status = self.status_combo_box.currentText()
        v_type = self.type_combo_box.currentText()
        print(f"[RepairView] Filtry GUI: status={status}, v_type={v_type}")
        self.request_vehicle_list.emit(status, v_type)

    def show_vehicle_list(self, vehicles_grouped):
        """Wyświetla listę pojazdów zwróconych przez serwis."""
        self.list_widget.clear()
        for (brand, model, cash_per_day), group in vehicles_grouped.items():
            count = len(group)
            display_text = f"{brand} {model} – {cash_per_day:.2f} zł/dzień - ({count} szt.)"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, group)
            self.list_widget.addItem(item)
        self.adjust_list_height()

    # ---------------- Sygnały do kontrolera ----------------
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
            self.show_repair_inputs(data)

            self.list_widget.setDisabled(True)

    def on_confirm_vehicle(self):
        vehicle_id = self.input_vehicle_id.text().capitalize()
        if vehicle_id:
            self.vehicle_id_entered.emit(vehicle_id)

    def on_submit_repair(self):
        vehicle_id = self.current_vehicle.vehicle_id
        try:
            repair_days = int(self.input_repair_days.text())
            repair_cost = int(self.input_repair_cost.text())
        except ValueError:
            repair_days = 0
            repair_cost < 0
        description = self.input_repair_desc.text()
        workshop_index = self.combo_workshop.currentIndex()
        self.submit_repair_info.emit(vehicle_id, repair_days, repair_cost, description, workshop_index)

    def on_rental_choice_clicked(self):
        choice = self.combo_rental_choice.currentText()
        self.rental_choice_selected.emit(choice)

    def on_replacement_choice_clicked(self):
        choice = self.combo_replacement_choice.currentText()
        self.replacement_choice_selected.emit(choice)

    def on_click_summary_button(self):
        self.click_summary_button.emit()

    # ---------------- Metody do aktualizacji GUI ----------------
    def show_repair_inputs(self, vehicle: Vehicle):
        self.current_vehicle = vehicle
        self.list_widget.clear()
        item_text = f"Wybrano: {vehicle.brand} {vehicle.vehicle_model} [{vehicle.individual_id}]"
        self.filters_group.hide()
        self.container_1.hide()
        self.container_2.show()
        self.list_widget.addItem(item_text)
        self.input_repair_days.show()
        self.input_repair_cost.show()
        self.input_repair_desc.show()
        self.combo_workshop.show()
        self.submit_repair_button.show()

    def show_rental_choice(self, rental):
        self.filters_group.hide()
        self.container_1.hide()
        self.container_2.hide()
        self.combo_rental_choice.show()
        self.rental_choice_button.show()

    def show_rental_repair_summary(self, replacement_vehicle):
        print(f"Strona view {replacement_vehicle=}")
        if not replacement_vehicle:
            self.list_widget.addItem("🚫 Brak równorzędnego pojazdu zastępczego.")
            return

        self.combo_replacement_choice.hide()
        self.replacement_choice_button.hide()
        self.list_widget.addItem(
            f"Wybrany pojazd zastępczy: {replacement_vehicle.brand} "
            f"{replacement_vehicle.vehicle_model} [{replacement_vehicle.individual_id}]"
        )
        self.adjust_list_height()
        self.summary_button.show()
        # self.finalize_button.show()

    def show_replacement_choice(self, replacement_vehicle):
        self.combo_replacement_choice.show()
        self.replacement_choice_button.show()

    def show_finished_rental(self, rental, invoice):
        print(f"{rental.reservation_id=}")
        print(f"{invoice.amount=}")
        self.list_widget.addItem(f"Zakończono wynajem pojazdu. Faktura: {invoice.amount if invoice else 'Brak'}")
        self.finalize_button.show()

    def show_swap_finished(self, result):
        rv = result["replacement_vehicle"]
        self.list_widget.addItem(f"Wydano pojazd zastępczy: {rv.brand} {rv.vehicle_model} [{rv.individual_id}]")
        self.finalize_button.show()

    def show_no_vehicle_available(self, choice):
        self.list_widget.addItem(f"Brak pojazdów do wyboru dla opcji: {choice}")
        self.finalize_button.show()

    def show_repair_finalized(self, repair):
        self.list_widget.addItem(f"Pojazd przekazany do warsztatu do dnia {repair.planned_return_date}")
        self.container_1.hide()
        self.container_2.hide()
        self.filters_group.hide()

    def load_workshops(self, workshops):
        self.combo_workshop.clear()
        for w in workshops:
            workshop_name = f"{w.first_name} {w.last_name}"
            self.combo_workshop.addItem(workshop_name, userData=w)

    def get_workshop_user(self, index):
        """Zwraca obiekt użytkownika warsztatu dla podanego indeksu comboboxa."""
        return self.combo_workshop.itemData(index)



    def adjust_list_height(self):
        count = self.list_widget.count()
        row_height = self.list_widget.sizeHintForRow(0) if count > 0 else 20
        frame = 2 * self.list_widget.frameWidth()
        new_height = min(10, max(5, count)) * row_height + frame
        self.list_widget.setMinimumHeight(new_height)
        self.list_widget.setMaximumHeight(new_height)