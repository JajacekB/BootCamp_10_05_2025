
from collections import defaultdict

from models.vehicle import Vehicle
from services.vehicle_avability import get_unavailable_vehicle, get_available_vehicles


class GetVehicleService:
    def __init__(self, session, view):
        self.session = session
        self.view = view

    def get_filtered_vehicles(self, status: str = "Dostepne", vehicle_type: str = "all"):

        if status == "Dostępne":
            vehicles = get_available_vehicles(self.session, vehicle_type=vehicle_type)

        elif status == "Niedostępne":
            vehicles, _ = get_unavailable_vehicle(self.session, vehicle_type=vehicle_type)

        elif status == "Nieaktywne":
            vehicles = self.session.query(Vehicle).filter(Vehicle.is_active == False).all()

        else:
            vehicles = (self.session.query(Vehicle).filter
                        (Vehicle.is_active == True,
                        Vehicle.type == vehicle_type
                        ).all())

        if not vehicles:
            print("\n🚫 Brak pasujących pojazdów.")
            self.view.show_errors("Brak pasujących pojazdów.")
            return

        vehicles_sorted = sorted(
            vehicles, key=lambda v: (v.cash_per_day, v.brand, v.vehicle_model, v.individual_id)
        )

        grouped = defaultdict(list)
        for v in vehicles_sorted:
            key = (v.brand, v.vehicle_model, v.cash_per_day)
            grouped[key].append(v)

        return grouped

