import sys
from datetime import date, timedelta

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QLabel, QComboBox,
        QGridLayout, QApplication, QListWidget, QListWidgetItem, QMessageBox, QLineEdit, QSizePolicy
    )
from PySide6.QtCore import Qt, QTimer

from gui.windows.get_vehicle_widget import GetVehicleWidget
from models.vehicle import Vehicle
from database.base import SessionLocal
from services.user_service import get_users_by_role
from services.vehicle_avability import get_available_vehicles
from repositories.get_methods import get_rental_for_vehicle, get_vehicle_by_id, get_replacement_vehicle
from repositories.repair_service import finalize_repair, finish_after_vehicle_swap, finish_broken_rental


class RepairVehicleWidget(QWidget):
    def __init__(self, session = None, user = None, controller = None):
        super().__init__()

        self.session = session or SessionLocal()
        self.user = user
        self.rental = None
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
        # self.confirm_button_1_1.clicked.connect(self.handle_choice_rental())
        self.hbox1.addWidget(self.confirm_button_1_1)

        self.confirm_button_1_2 = QPushButton("Zatwierdź")
        self.confirm_button_1_2.setFixedSize(150, 45)
        self.confirm_button_1_2.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_1_2.hide()
        # self.confirm_button_1_2.clicked.connect(self.on_replacement_option_selected())
        self.hbox1.addWidget(self.confirm_button_1_2)

        self.confirm_button_1_3 = QPushButton("Zatwierdź")
        self.confirm_button_1_3.setFixedSize(150, 45)
        self.confirm_button_1_3.setStyleSheet(
            "background-color: grey;"
            " font-size: 22px; color: white;"
        )
        self.confirm_button_1_3.hide()
        # self.confirm_button_1_3.clicked.connect(self.on_cheaper_decision())
        self.hbox1.addWidget(self.confirm_button_1_3)

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
        self.confirm_button_2_1.clicked.connect(self.on_replacement_option_selected)
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
        vehicle = get_vehicle_by_id(self.session, vehicle_id)

        if vehicle:
            self.current_vehicle = vehicle
            self.process_vehicle(vehicle)

        else:
            QMessageBox.warning(self, "Nie znaleziono", f"Brak pojazdu o ID {vehicle_id}.")

    def process_vehicle(self, vehicle: Vehicle):

        print("🔧 step 2")

        self.vehicle = vehicle
        self.get_vehicle_widget.vehicle_list.clear()
        self.get_vehicle_widget.filters_group.hide()

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

        self.container_hbox1.show()
        self.container_hbox2.show()
        self.confirm_button_3_1.clicked.connect(self.handle_data_1)
        self.container_hbox3.show()


    def handle_data_1(self):
        # Wywołana przez: self.confirm_button_3_1.clicked.connect(self.handle_data_1)

        print("🔧 step 3")

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
            self.comment_label_0.setText("Błąd, Liczba dni musi być liczbą całkowią większą od 0")
            self.input_area_0.clear()
            return

        repair_rates_input = self.input_area_2.text()
        try:
            repair_rates = int(repair_rates_input)
            if repair_rates < 0:
                self.comment_label_2.setText("Błąd, koszt nie może być mniejszy od 0")
                self.input_area_0.clear()
                return
            self.repair_rates = repair_rates
        except ValueError:
            self.comment_label_2.setText("Błąd, Koszt naprawy musi byc liczną")
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

        self.planned_return_date = date.today() + timedelta(days=repair_days)
        self.rental = get_rental_for_vehicle(
            session=self.session,
            vehicle_id=self.vehicle.id,
            planned_return_date=self.planned_return_date
        )

        if not self.rental:

            print("🔧 step 4a")
            print("Tylko początek naprawy")
            self.on_finalize_clicked()
            return True

        print("🔧 step 4b")

        self.container_hbox0.hide()
        self.container_hbox2.hide()
        self.container_hbox3.hide()


        self.container_hbox1.show()
        self.comment_label_1.setText("Czy klient kontynuuje wynajem?")
        self.combo_area_1.clear()
        self.combo_area_1.addItems(["Kontynuuje wynajem", "Kończy wynajem"])
        self.confirm_button_1_1.clicked.connect(self.handle_choice_rental)
        self.confirm_button_1_1.show() # button przekierowuje do handle_choice_rental
        return None


    def handle_choice_rental(self):

        print("🔧 step 5b")

        index = self.combo_area_1.currentText()

        if index == "Kończy wynajem":
            print("Koniec najmu i początek naprawy")
            return self.handle_finish_broken_rental()


        self.start_date = date.today()
        self.planned_return_date = date.today() + timedelta(days=self.repair_days)
        # self.planned_return_date = self.planned_return_date

        replacement_vehicle_list = get_available_vehicles(self.session, self.start_date, self.planned_return_date, self.vehicle.type)
        self.replacement_vehicle = next(
            (v for v in replacement_vehicle_list if v.cash_per_day == self.vehicle.cash_per_day), None
        )

        if self.replacement_vehicle:
            final_text_0 = " "
            final_text_1 = (
                f"Wydano klientowi pojazd zastępczy 1: {self.replacement_vehicle.brand} "
                f"{self.replacement_vehicle.vehicle_model} {self.replacement_vehicle.individual_id}"
            )
            self.get_vehicle_widget.vehicle_list.addItem(final_text_0)
            self.get_vehicle_widget.vehicle_list.addItem(final_text_1)
            self.get_vehicle_widget.adjust_list_height()

            print("Nowy rental -  pojazd z tej samej kategori cenowej, koniec najmu i początek naprawy")
            self.on_finish_swap_clicked()

            # self.on_finalize_clicked()
            return True

        self.container_hbox0.hide()
        self.container_hbox2.hide()
        self.container_hbox3.hide()

        self.comment_label_1.clear()
        self.comment_label_1.setText("Brak pojazdu w tym samym standardzie.\nJaki pojazd wybiera klient?")

        self.combo_area_1.clear()
        self.combo_area_1.addItems(["Droższy", "Tańszy", "Anuluje wynajem"])

        self.confirm_button_1_1.hide()
        self.confirm_button_1_2.clicked.connect(self.on_replacement_option_selected)
        self.confirm_button_1_2.show()
        print("Pyrażka !!!")

        return True

    def on_replacement_option_selected(self):

        index = self.combo_area_1.currentText()

        if index == "Anuluje wynajem":
            self.handle_finish_broken_rental()

        elif index == "Tańszy":

            lower_price_vehicle = get_replacement_vehicle(self.session, self.vehicle, self.planned_return_date, True)
            if lower_price_vehicle:
                print(f"\nWydano klientowi pojazd zastępczy - lower: {lower_price_vehicle} \nOddano do naprawy: {self.vehicle}")
                self.on_finish_swap_clicked()
                # self.on_finalize_clicked()
                return True
            else:
                higher_price_vehicle = get_replacement_vehicle(self.session, self.vehicle, self.planned_return_date, False)
                print("\nBrak tańszego pojazdu. Wydano droższy bez naliczania dodatkowych kosztów.")
                if higher_price_vehicle:
                    print(
                        f"\nWydano klientowi pojazd zastępczy  higher a miał byc lower: {higher_price_vehicle} \nOddano do naprawy: {self.broken_veh}")
                    self.on_finish_swap_clicked()
                    # self.on_finalize_clicked()
                    return True
                else:
                    return self.handle_finish_broken_rental()

        elif index == "Droższy":
            higher_price_vehicle = get_replacement_vehicle(self.session, self.vehicle, self.planned_return_date, False)
            if higher_price_vehicle:
                print(f"\nWydano klientowi pojazd zastępczy higher: {higher_price_vehicle} \nOddano do naprawy: {self.vehicle}")
                self.on_finish_swap_clicked()
                # self.on_finalize_clicked()
                return True
            else:

                self.comment_label_1.clear()
                self.comment_label_1.setText("Brak pojazdów o wyższym standardzie.\nCzy klient decyduje się na tańszy z rabatem?")

                self.combo_area_1.clear()
                self.combo_area_1.addItems(["Decyduje się na tańszy", "Anuluje wynajem"])

                self.confirm_button_1_2.hide()
                self.confirm_button_1_3.clicked.connect(self.on_cheaper_decision)
                self.confirm_button_1_3.show()


    def on_cheaper_decision(self):

        index = self.combo_area_1.currentText()

        if index == "Anuluje wynajem":
            return self.handle_finish_broken_rental()

        else:
            lower_price_vehicle = get_replacement_vehicle(self.session, self.vehicle, self.planned_return_date, True)
            if lower_price_vehicle:
                print(
                    f"\nWydano klientowi pojazd zastępczy lower a miał byc higher: {lower_price_vehicle} \nOddano do naprawy: {self.vehicle}")
                self.on_finish_swap_clicked()
                # self.on_finalize_clicked()
                return True
            else:
                return self.on_finalize_clicked()


    def on_finish_swap_clicked(self):
        try:
            result = finish_after_vehicle_swap(
                self.session,
                self.vehicle,
                self.replacement_vehicle,
                self.rental,
                different_price=False
            )
            print("Knoniec starego najmu, początek nowego ")
            replacement_vehicle = result["replacement_vehicle"]
            broken_cost = result["broken_veh_cost"]

            # GUI: aktualizacja listy i informacji
            self.get_vehicle_widget.vehicle_list.addItem(" ")
            self.get_vehicle_widget.vehicle_list.addItem(
                f"Wydano pojazd zastępczy,  dlaczego drugi raz: {replacement_vehicle.brand} "
                f"{replacement_vehicle.vehicle_model} {replacement_vehicle.individual_id}"
            )
            self.get_vehicle_widget.adjust_list_height()

            # brak aktualizacji "Monitora"

            finalize_repair(
                self.session,
                self.vehicle,
                self.work_user,
                self.planned_return_date,
                self.total_cost,
                self.description
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Błąd zapisu repair po wymianie",
                f"Nie udało się zapisać zmian w bazie.\n\nSzczegóły: {e}"
            )
        return True

    def handle_finish_broken_rental(self):

        try:
            rental, invoice = finish_broken_rental(self.session, self.vehicle)
            if not rental or not invoice:
                QMessageBox.warning(self, "Błąd", "Nie znaleziono faktury dla tego wynajmu.")
                return

            final_text_0 = " "
            final_text_1 = f"Zakończono wynajem pojazdu: {self.vehicle.brand} {self.vehicle.vehicle_model} {self.vehicle.individual_id}"
            self.get_vehicle_widget.vehicle_list.addItem(final_text_0)
            self.get_vehicle_widget.vehicle_list.addItem(final_text_1)
            self.get_vehicle_widget.adjust_list_height()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Błąd zapisu zakończenia wynajmu przed czasem",
                f"Nie udało się zapisać zmian w bazie.\n\nSzczegóły: {e}"
            )

        return self.on_finalize_clicked()


    def on_finalize_clicked(self):
        try:
            repair = finalize_repair(
                self.session,
                self.vehicle,
                self.work_user,
                self.planned_return_date,
                self.total_cost,
                self.description
            )

            # 👇 teraz GUI robi swoje
            self.container_hbox0.hide()
            self.container_hbox1.hide()
            self.container_hbox2.hide()
            self.container_hbox3.hide()

            self.get_vehicle_widget.vehicle_list.addItem(" ")
            self.get_vehicle_widget.vehicle_list.addItem(
                f"Pojazd: {self.vehicle.brand} {self.vehicle.vehicle_model} {self.vehicle.individual_id}"
            )
            self.get_vehicle_widget.vehicle_list.addItem(
                f"przekazany do warsztatu: {self.work_user.first_name} {self.work_user.last_name} "
                f"do dnia {self.planned_return_date}."
            )
            self.get_vehicle_widget.adjust_list_height()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Błąd zapisu - tylko naprawa",
                f"Nie udało się zapisać zmian w bazie.\n\nSzczegóły: {e}"
            )
        return True




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RepairVehicleWidget()
    main_window.showMaximized()
    sys.exit(app.exec())
