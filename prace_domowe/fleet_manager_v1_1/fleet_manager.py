from fleet_vehicle import Car, Scooter, Bike


class FleetManager():
    def __init__(self):
        self.vehicles = []

    def generate_id(self,prefix):
        max_num = 0
        for vehicle in self.vehicles:
            vid = vehicle.vehicle_id.lower()
            if vid.startswith(prefix.lower()):
                try:
                    number_part = int(vid[len(prefix):])
                    if number_part > max_num:
                        max_num = number_part
                except ValueError:
                    pass

        next_num = max_num + 1
        return f"{prefix}{next_num:03d}"

    def add_vehicle(self):

        type_prefix_map = {
            "car": "C",
            "scooter": "S",
            "bike": "B"
        }

        while True:
            vehicle_type = input("\nPodaj typ pojazdu (car/scooter/bike): ").strip().lower()
            if vehicle_type in type_prefix_map:
                prefix = type_prefix_map[vehicle_type]
            else:
                print("\nNiepoprawny typ pojazdu, spróbuj jeszcze raz.")
                continue

            vehicle_id = self.generate_id(prefix)

            if vehicle_type == "car":

                brand = input("\nPodaj producenta pojazdu: ").strip()
                cash_per_day = float(input("\nPodaj cenę najmu za jedną dobę: ").strip())
                size = input("\nPodaj rozmiar samochodu (miejski, kompakt, limuzyna, SUV mały, SUV: ").strip()
                fuel_type = input("\nPodaj rodzaj paliwa: ").strip()
                vehicle = Car(vehicle_id, brand, cash_per_day, True, size, fuel_type)

            elif vehicle_type == "scooter":

                brand = input("\nPodaj producenta pojazdu: ").strip()
                cash_per_day = float(input("\nPodaj cenę najmu za jedną dobę: ").strip())
                max_speed = input("\npodaj prędkość maksymalną: ").strip()
                vehicle = Scooter(vehicle_id, brand, cash_per_day, True, max_speed)

            elif vehicle_type == "bike":

                brand = input("\nPodaj producenta pojazdu: ").strip()
                cash_per_day = float(input("\nPodaj cenę najmu za jedną dobę: ").strip())
                bike_type = input("\nPodaj rodzaj typ roweru: ").strip()
                is_electric = bool(input("\nCzy rower jest elektryczny: ").strip())
                is_electric_bool = is_electric in ("tak", "t", "yes", "y")
                vehicle = Bike(vehicle_type, brand, cash_per_day, bike_type, is_electric_bool)

            print(f"\nCzy chcesz dodać pojazd: - {vehicle}? (Tak/Nie): ")
            choice = input().strip().lower()

            if choice in ("tak", "t", "yes", "y"):
                self.vehicles.append(vehicle)
                print("\nOperacja dodawania pojazdu zakończona sukcesem")
                break
            elif choice in ("nie", "n", "no"):
                print("\nWprowadzanie pojazdu anulowane. Spróbuj jeszcze raz.")
            else:
                print("\nNiepoprawna odpowiedź. Spróbuj ponownie.")

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

