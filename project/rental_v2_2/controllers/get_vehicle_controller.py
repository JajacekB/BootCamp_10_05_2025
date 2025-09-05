# controllers.get_vehicle_controller.py
from PySide6.QtCore import Slot

from models.vehicle import Vehicle
from repositories.get_vehicle_service import GetVehicleService
from repositories.read_methods import get_rentals_by_vehicle_id, get_repairs_by_vehicle_id


class GetVehicleController:
    def __init__(self, session, view):
        self.service = GetVehicleService(session, view)
        self.session = session
        self.view = view


        self.view.request_vehicle_list.connect(self.request_vehicle_list)
        self.view.vehicle_selected.connect(self.on_vehicle_item_clicked)

    @Slot(str, str, str)
    def request_vehicle_list(self, status: str = "Dostępne", v_type: str = "Wszystkie", role: str = "client"):

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
            if role == "client":
                self.view.show_vehicle_list_readonly(vehicles_grouped)
            else:
                self.view.show_vehicle_list(vehicles_grouped)
        else:
            self.view.show_errors("Brak pasujących pojazdów.")

    def on_vehicle_item_clicked(self, vehicle: Vehicle):
        rentals = get_rentals_by_vehicle_id(self.session, vehicle)
        repairs = get_repairs_by_vehicle_id(self.session, vehicle)
        self.view.show_vehicle_history(vehicle, rentals, repairs)


