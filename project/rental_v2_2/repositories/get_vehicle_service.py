# repositories.get_vehicle_service import GetVehicleService
from collections import defaultdict

from models.user import User
from models.vehicle import Vehicle
from models.rental_history import RentalHistory
from models.repair_history import RepairHistory
from services.vehicle_avability import get_unavailable_vehicle, get_available_vehicles
from gui.widgets.get_vehicle_view import GetVehicleView


class GetVehicleService:
    def __init__(self, session, view):
        self.session = session
        self.view = view



    def get_filtered_vehicles(self, status: str, vehicle_type: str):

        if status == "Dostępne":
            vehicles = get_available_vehicles(self.session, vehicle_type=vehicle_type)

        elif status == "Niedostępne":
            vehicles, _ = get_unavailable_vehicle(self.session, vehicle_type=vehicle_type)

        else:
            if vehicle_type == "all":
                vehicles = self.session.query(Vehicle).all()

            else:
                vehicles = self.session.query(Vehicle).filter(Vehicle.type == vehicle_type).all()

        if not vehicles:
            print("\n🚫 Brak pasujących pojazdów.")
            self.view.show_errors(["Brak pasujących pojazdów."])
            return

        vehicles_sorted = sorted(
            vehicles, key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model, v.individual_id)
        )

        grouped = defaultdict(list)
        for v in vehicles_sorted:
            key = (v.brand, v.vehicle_model, v.cash_per_day)
            grouped[key].append(v)

        return grouped

