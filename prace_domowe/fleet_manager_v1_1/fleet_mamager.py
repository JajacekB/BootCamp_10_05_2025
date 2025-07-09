

class FleetManager():
    def __init__(self):
        self.vehicles = []

    def generate_id(self,vehicle):
        pass

    def add_vehicle(self,vehicle):
        pass

    def remove_vehicle(self,vehicle_id):
        pass

    def get_all_vehicles(self):
        if not self.vehicles:
            print("\nNie ma jeszcze pojazdów w wypożyczalni.")
        else:
            print("\nLista pojazdów:\n")
            for vehicle in self.vehicles:
                print(vehicle)

    def get_available_vehicles(self):
        pass

    def get_rented_vehicles(self):
        pass

    def get_vehicles_by_id(self):
        pass

    def get_vehicles_by_date(self):
        pass

    def get_vehicles_by_type(self):
        pass

