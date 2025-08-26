# repair_controller.py
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QMessageBox
from datetime import date, timedelta

from models.vehicle import Vehicle
from services.user_service import get_users_by_role
from repositories.repair_service import RepairService
from repositories.read_methods import get_rental_for_vehicle, get_vehicle_by_id, get_replacement_vehicle
from services.vehicle_avability import get_available_vehicles


class RepairController:
    def __init__(self, session, view):
        self.session = session
        self.view = view
        self.service = RepairService(session)

        # Podłącz sygnały z widoku
        self.view.vehicle_selected.connect(self.on_vehicle_item_clicked)
        # self.view.vehicle_selected.connect(self.on_vehicle_selected)
        self.view.vehicle_id_entered.connect(self.on_vehicle_id_entered)
        self.view.click_summary_button.connect(self.on_confirm_rental_replacement)
        self.view.request_vehicle_list.connect(self.request_vehicle_list)
        self.view.submit_repair_info.connect(self.on_submit_repair_info)
        self.view.rental_choice_selected.connect(self.on_rental_choice_selected)
        self.view.replacement_choice_selected.connect(self.on_replacement_choice_selected)
        self.view.finalize_repair_signal.connect(self.on_finalize_repair)

    @Slot(str, str)
    def request_vehicle_list(self, status: str = "Wszystkie", v_type: str = "Wszystkie"):

        print(f"[RepairController] Filtry GUI: status={status}, v_type={v_type}")

        type_map = {
            "Wszystkie": "all",
            "Samochody": "car",
            "Skutery": "scooter",
            "Rowery": "bike"
        }
        vehicle_type = type_map.get(v_type, "all")

        vehicles_grouped = self.service.get_filtered_vehicles(status, vehicle_type)

        if vehicles_grouped:
            self.view.show_vehicle_list(vehicles_grouped)
        else:
            self.view.vehicle_list.clear()
            self.view.vehicle_list.addItem("🚫 Brak pasujących pojazdów.")

    def on_vehicle_item_clicked(self, vehicle: Vehicle):
        print("on_vehicle_item_clicked")
        self.view.show_repair_inputs(vehicle)
        # vehicle = item.data(Qt.UserRole)
        if not vehicle:
            return
        self.current_vehicle = vehicle
        self.view.show_repair_inputs(vehicle)
        workshops = get_users_by_role(self.session, "workshop")
        self.view.load_workshops(workshops)

    def on_vehicle_selected(self, vehicle: Vehicle):
        self.current_vehicle = vehicle
        self.view.show_repair_inputs(vehicle)

    def on_vehicle_id_entered(self, vehicle_id: str):
        vehicle = get_vehicle_by_id(self.session, vehicle_id)
        if not vehicle:
            QMessageBox.warning(self.view, "Nie znaleziono pojazdu", f"Brak pojazdu o ID {vehicle_id}")
            return
        self.current_vehicle = vehicle
        self.view.show_repair_inputs(vehicle)
        workshops = get_users_by_role(self.session, "workshop")
        self.view.load_workshops(workshops)

    def on_submit_repair_info(self, vehicle_id, repair_days, repair_rates, description, workshop_index):
        vehicle = get_vehicle_by_id(self.session, vehicle_id)
        if not vehicle:
            QMessageBox.warning(self.view, "Nie znaleziono pojazdu", f"Brak pojazdu o ID {vehicle_id}")
            return

        self.current_vehicle = vehicle
        self.repair_days = repair_days
        self.total_cost = repair_rates
        self.description = description
        self.work_user = self.view.get_workshop_user(workshop_index)

        self.planned_return_date = date.today() + timedelta(days=repair_days)

        self.rental = get_rental_for_vehicle(self.session, vehicle.id, self.planned_return_date)

        if not self.rental:

            repair = self.service.finalize_repair(
                self.current_vehicle,
                self.work_user,
                self.planned_return_date,
                self.total_cost,
                self.description
            )
            self.view.show_repair_finalized(repair)
            return

        self.view.show_rental_choice(self.rental)

    def on_rental_choice_selected(self, choice):
        if choice == "Kończy wynajem":
            rental, invoice = self.service.finish_broken_rental(self.current_vehicle)
            print(f"1 {invoice.amount=}")
            self.view.show_finished_rental(rental, invoice)
        else:
            self.start_date = date.today()
            self.replacement_vehicle = next(
                (v for v in get_available_vehicles(self.session, self.start_date, self.planned_return_date,
                                                self.current_vehicle.type)
                if v.cash_per_day == self.current_vehicle.cash_per_day),
                None
            )
            if self.replacement_vehicle:
                print(f"{self.replacement_vehicle=}")
                self.view.show_rental_repair_summary(self.replacement_vehicle)
            else:
                self.view.show_replacement_choice(None)

    def on_confirm_rental_replacement(self):

        if not self.replacement_vehicle or not self.current_vehicle:
            return

        result = self.service.finish_after_vehicle_swap(
            broken_vehicle=self.current_vehicle,
            replacement_vehicle=self.replacement_vehicle,
            old_rental=self.rental,
            different_price=False
        )

        self.view.list_widget.addItem(
            f"Odany do warsztatu: {self.current_vehicle.brand} {self.current_vehicle.vehicle_model} "
            f"[{self.current_vehicle.individual_id}]."
        )
        self.view.list_widget.addItem(
            f"Wydany klientowi: {self.replacement_vehicle.brand} {self.replacement_vehicle.vehicle_model} "
            f"[{self.replacement_vehicle.individual_id}]."
        )
        self.view.adjust_list_height()
        self.view.combo_rental_choice.hide()
        self.view.rental_choice_button.hide()
        self.view.summary_button.hide()
        self.view.finalize_button.show()

    def on_replacement_choice_selected(self, choice):
        if choice in ["Droższy", "Tańszy"]:
            cheaper = choice == "Tańszy"
            replacement_vehicle = get_replacement_vehicle(
                self.session,
                self.current_vehicle,
                self.planned_return_date,
                prefer_cheaper=cheaper
            )

            if replacement_vehicle:
                # standardowa zamiana pojazdów
                result = self.service.finish_after_vehicle_swap(
                    self.current_vehicle,
                    replacement_vehicle,
                    self.rental,
                    different_price=not cheaper  # droższy → True, tańszy → False
                )
                self.view.show_swap_finished(result)

                if cheaper:
                    self.view.list_widget.addItem("✅ Otrzymałeś tańszy pojazd – koszty zostały obniżone.")
                    self.view.adjust_list_height()
                else:
                    self.view.list_widget.addItem("✅ Otrzymałeś droższy pojazd – koszty zostały podniesione.")
                    self.view.adjust_list_height()
            else:
                # fallback logic
                if cheaper:
                    # klient chciał tańszy, brak → daj droższy po obecnych kosztach
                    replacement_vehicle = get_replacement_vehicle(
                        self.session,
                        self.current_vehicle,
                        self.planned_return_date,
                        prefer_cheaper=False
                    )
                    if replacement_vehicle:
                        result = self.service.finish_after_vehicle_swap(
                            self.current_vehicle,
                            replacement_vehicle,
                            self.rental,
                            different_price=False  # koszty po obecnym pojeździe
                        )
                        self.view.show_swap_finished(result)
                        self.view.list_widget.addItem(
                            "ℹ️ Nie było tańszego pojazdu – otrzymałeś droższy, ale koszty pozostają bez zmian.")
                        self.view.adjust_list_height()
                    else:
                        self.view.show_no_vehicle_available("Brak pojazdu zastępczego")
                else:
                    # klient chciał droższy, brak → daj tańszy i licz cały okres po tańszym
                    replacement_vehicle = get_replacement_vehicle(
                        self.session,
                        self.current_vehicle,
                        self.planned_return_date,
                        prefer_cheaper=True
                    )
                    if replacement_vehicle:
                        result = self.service.finish_after_vehicle_swap(
                            self.current_vehicle,
                            replacement_vehicle,
                            self.rental,
                            different_price=False  # koszt całego okresu liczony po tańszym
                        )
                        self.view.show_swap_finished(result)
                        self.view.list_widget.addItem(
                            "ℹ️ Nie było droższego pojazdu – otrzymałeś tańszy, koszty policzono według tańszego pojazdu."
                        )
                        self.view.adjust_list_height()
                    else:
                        self.view.show_no_vehicle_available("Brak pojazdu zastępczego")
        else:  # Anuluje wynajem
            rental, invoice = self.service.finish_broken_rental(self.current_vehicle)
            self.view.show_finished_rental(rental, invoice)

    def on_finalize_repair(self):
        repair = self.service.finalize_repair(
            self.current_vehicle,
            self.work_user,
            self.planned_return_date,
            self.total_cost,
            self.description
        )
        self.view.show_repair_finalized(repair)

    def get_workshop_user(self, index):
        workshops = get_users_by_role(self.session, "workshop")
        self.view.load_workshops(workshops)