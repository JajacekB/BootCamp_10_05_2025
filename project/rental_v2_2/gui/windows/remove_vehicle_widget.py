import sys
from collections import defaultdict
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox, QSpacerItem, QSizePolicy, QHBoxLayout
    )
from PySide6.QtCore import Qt, QTimer, Signal

from services.vehicle_avability import get_available_vehicles

from models.vehicle import Vehicle, Car, Scooter, Bike
from models.user import User
from models.rental_history import RentalHistory
from database.base import SessionLocal


class RemoveVehicleWidget(QWidget):

    def __init__(self, session=None, role="client"):
        super().__init__()
        self.session =  session or SessionLocal()
        self.role = role
        self.vehicle_type = None

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

        form_layout = QFormLayout()
        form_layout.addRow("Jaki rodzaj pojazdu chcesz usunąć:", self.type_combo_box)

        self.main_layout.addLayout(form_layout)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.handle_item_clicked)
        self.main_layout.addWidget(self.list_widget)

        self.search_button = QPushButton("Pokaż")
        self.search_button.setStyleSheet(
            "background-color: green;"
            " font-size: 24px; color: white;"
            " border-radius: 8px; padding: 10px; ")
        self.search_button.setFixedSize(150, 45)
        self.search_button.clicked.connect(self.get_available_veh_list)
        self.main_layout.addWidget(self.search_button, alignment=Qt.AlignRight)

        self.confirmation_widget = QWidget()
        self.confirmation_layout = QVBoxLayout(self.confirmation_widget)

        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.confirmation_layout.addWidget(self.info_label)

        buttons_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Potwierdź usunięcie")
        self.cancel_button = QPushButton("Anuluj")
        buttons_layout.addWidget(self.confirm_button)
        buttons_layout.addWidget(self.cancel_button)
        self.confirmation_layout.addLayout(buttons_layout)

        self.main_layout.addWidget(self.confirmation_widget)
        self.confirmation_widget.setVisible(False)

        # Podłączamy sygnały przycisków
        self.confirm_button.clicked.connect(self._confirm_delete)
        self.cancel_button.clicked.connect(self._cancel_delete)

        # zmienna do przechowywania pojazdu do usunięcia
        self.vehicle_to_delete = None

        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def get_available_veh_list(self):
        self.list_widget.clear()

        vehicle_type_input = self.type_combo_box.currentText()

        vehicle_type_options = {
            "Wszystkie": "all",
            "Samochody": "car",
            "Skutery": "scooter",
            "Rowery": "bike"
        }
        vehicle_type = vehicle_type_options.get(vehicle_type_input, "all")

        available_vehicles = get_available_vehicles(self.session, vehicle_type=vehicle_type)

        vehicles_sorted = sorted(
            available_vehicles,
            key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model, v.individual_id)
        )
        vehicles = defaultdict(list)
        for v in (vehicles_sorted):
            key = (v.brand, v.vehicle_model, v.cash_per_day)
            vehicles[key].append(v)

        for (brand, model, cash_per_day), group in vehicles.items():
            count = len(group)
            display_text = f"{brand} {model}  –  {cash_per_day:.2f} zł/dzień - ({count} szt.)"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, group)
            self.list_widget.addItem(item)

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

    # def confirm_and_delete(self, vehicle):
    #     msg = QMessageBox(self)
    #     msg.setIcon(QMessageBox.Warning)
    #     msg.setWindowTitle("Potwierdzenie usunięcia")
    #     msg.setText(f"Czy na pewno chcesz usunąć ten pojazd?\n\n{vehicle!r}")
    #     msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    #     msg.setDefaultButton(QMessageBox.No)
    #
    #     result = msg.exec()
    #
    #     if result == QMessageBox.Yes:
    #         self.session.delete(vehicle)
    #         self.session.commit()
    #         QMessageBox.information(self, "Usunięto", "Pojad został usunięty z bazy pojazdów.")
    #         self.get_available_veh_list()

    def handle_item_clicked(self, item):
        data = item.data(Qt.UserRole)

        if data == "return":
            self.get_available_veh_list()  # wróć do widoku grup
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

        # Ukrywamy listę, pokazujemy panel potwierdzenia
        self.list_widget.setEnabled(False)
        self.confirmation_widget.setVisible(True)

        # Wypełniamy label informacjami o pojeździe
        self.info_label.setText(
            f"Czy na pewno chcesz usunąć ten pojazd?\n\n{vehicle.get_display_info()}"
        )

        # Zapamiętujemy pojazd do usunięcia
        self.vehicle_to_delete = vehicle

    def _confirm_delete(self):
        if not self.vehicle_to_delete:
            return
        try:
            self.session.delete(self.vehicle_to_delete)
            self.session.commit()
            QMessageBox.information(self, "Sukces", "Pojazd został usunięty.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć pojazdu:\n{str(e)}")

        self._reset_after_delete()

    def _cancel_delete(self):
        self._reset_after_delete()

    def _reset_after_delete(self):
        # Reset widoku: ukryj panel potwierdzenia, włącz listę, wyczyść zmienną
        self.confirmation_widget.setVisible(False)
        self.list_widget.setEnabled(True)
        self.vehicle_to_delete = None
        self.get_available_veh_list()

    # def handle_single_vehicle_click(self, item):
    #     vehicle = item.data(Qt.UserRole)
    #
    #     if isinstance(vehicle, list):
    #         self.show_group_members(vehicle)
    #         self.list_widget.itemClicked.disconnect()
    #         self.list_widget.itemClicked.connect(self.handle_single_vehicle_click)
    #         return
    #
    #     if not vehicle:
    #         QMessageBox.information(self, "Informacja", item.text())
    #         return
    #
    #     msg = QMessageBox(self)
    #     msg.setWindowTitle("Potwierdź usunięcie pojazdu")
    #     msg.setText("Czy na pewno chcesz usunąć ten pojazd?\n\n" + vehicle.get_display_info())
    #     msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    #     msg.setIcon(QMessageBox.Warning)
    #     result = msg.exec()
    #
    #     if result == QMessageBox.Yes:
    #         try:
    #             self.session.delete(vehicle)
    #             self.session.commit()
    #             QMessageBox.information(self, "Sukces", "Pojazd został usunięty.")
    #             self.get_available_veh_list()
    #         except Exception as e:
    #             QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć pojazdu:\n{str(e)}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RemoveVehicleWidget()
    main_window.show()
    sys.exit(app.exec())