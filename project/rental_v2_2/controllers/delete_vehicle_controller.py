from PySide6.QtCore import Slot
from collections import defaultdict

from repositories.write_methods import deactivate_vehicle
from services.vehicle_avability import get_available_vehicles


class DeleteVehicleController():
    def __init__(self, session, view):

        self.session = session
        self.view = view

        self.view.request_vehicle_list.connect(self.handle_vehicle_list)
        self.view.request_delete_vehicle.connect(self.handle_delete_vehicle)

    @Slot(str)
    def handle_vehicle_list(self, v_type: str = "Wszystkie"):

        print(f"[RepairController] Filtry GUI: v_type={v_type}")

        type_map = {
            "Wszystkie": "all",
            "Samochody": "car",
            "Skutery": "scooter",
            "Rowery": "bike"
        }
        vehicle_type = type_map.get(v_type, "all")
        vehicles = get_available_vehicles(self.session, vehicle_type=vehicle_type)
        vehicles_sorted = sorted(
            vehicles, key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model, v.individual_id)
        )

        vehicles_grouped = defaultdict(list)
        for v in vehicles_sorted:
            key = (v.brand, v.vehicle_model, v.cash_per_day)
            vehicles_grouped[key].append(v)

        if vehicles_grouped:
            self.view.show_vehicle_list(vehicles_grouped)
        else:
            self.view.show_errors("Brak wolnych pojazdów.")

    @Slot(object)
    def handle_delete_vehicle(self, vehicle_to_delete):

        success, text = deactivate_vehicle(self.session, vehicle_to_delete)
        if success:
            self.view.success_deactivate(text)
        else:
            self.view.error_deactivate(text)

