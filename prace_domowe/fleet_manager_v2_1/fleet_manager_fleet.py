from fleet_models_db import Vehicle, Car, Scooter, Bike
from sqlalchemy import func, cast, Integer
from fleet_database import Session

def generate_vehicle_id(session, prefix: str) -> str:
    prefix_len = len(prefix)
    prefix_upper = prefix.upper()

    max_number = session.query(
        func.max(
            cast(func.substr(Vehicle.vehicle_id, prefix_len + 1), Integer)
        )
    ).filter(
        Vehicle.vehicle_id.ilike(f"{prefix_upper}%")
    ).scalar()

    if max_number is None:
        max_number = 0

    next_number = max_number + 1
    new_vehicle_id = f"{prefix_upper}{next_number:03d}"
    return new_vehicle_id

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())
            if value > 0:
                return value
            else:
                print("❌ Liczba musi być większa od zera.")
        except ValueError:
            print("❌ Wprowadź poprawną liczbę całkowitą (np. 25).")

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value > 0:
                return value
            else:
                print("❌ Liczba musi być większa od zera.")
        except ValueError:
            print("❌ Wprowadź poprawną liczbę całkowitą (np. 25).")

def add_vehicle():

    type_prefix_map = {
        "car": "C",
        "scooter": "S",
        "bike": "B"
    }

    while True:
        vehicle_type = input("\nPodaj typ pojazdu (car, scooter, bike): ").strip().lower()
        if vehicle_type in type_prefix_map:
            prefix = type_prefix_map[vehicle_type]
            break
        else:
            print("\nNiepoprawny typ pojazdu. Spróbuj jeszcze raz")
            continue

    with Session() as session:

        vehicle_id = generate_vehicle_id(session, prefix)

        brand = input("\nPodaj producenta pojazdu: ").strip().capitalize()
        vehicle_model = input("\nPodaj model:").strip().capitalize()
        cash_per_day = get_positive_float("\nPodaj cenę najmu za jedną dobę: ")

        if vehicle_type == "car":

            size = input(
                "\nPodaj rozmiar samochodu (Miejski, Kompakt, Limuzyna, CrossOver, SUV): ").strip().capitalize()
            fuel_type = input("\nPodaj rodzaj paliwa: ").strip()
            vehicle = Car(
                vehicle_id=vehicle_id,
                brand=brand,
                vehicle_model=vehicle_model,
                cash_per_day=cash_per_day,
                size=size,
                fuel_type=fuel_type
            )

        elif vehicle_type == "scooter":

            max_speed = get_positive_int("\nPodaj prędkość maksymalną (km/h): ")
            vehicle = Scooter(
                vehicle_id=vehicle_id,
                brand=brand,
                vehicle_model=vehicle_model,
                cash_per_day=cash_per_day,
                max_speed=max_speed
            )

        elif vehicle_type == "bike":

            bike_type = input("\nPodaj typ roweru (Szosowy, Miejski, MTB): ").strip().capitalize()
            electric_input = input("\nCzy rower jest elektryczny: ").strip().lower()
            is_electric_bool = electric_input in ("tak", "t", "yes", "y")
            vehicle = Bike(
                vehicle_id=vehicle_id,
                brand=brand,
                vehicle_model=vehicle_model,
                cash_per_day=cash_per_day,
                bike_type=bike_type,
                is_electric=is_electric_bool
            )
        while True:
            print(f"\nCzy chcesz dodać pojazd?  {vehicle}")
            choice = input("(Tak/Nie): ").strip().lower()
            if choice in ("tak", "t", "yes", "y"):
                session.add(vehicle)
                session.commit()
                session.refresh(vehicle)
                print(f"\n✅ Pojazd {vehicle} został dodany pomyślnie.")
                return vehicle
            elif choice in ("nie", "n", "no"):
                print("\nWprowadzanie pojazdu anulowane.")
                return None
            else:
                print("\nNiepoprawna odpowiedź. Wpisz 'tak' lub 'nie'.")

def get_vehicle():
    print(">>> [MOCK] Przeglądanie pojazdów...")

def borrow_vehicle():
    print(">>> [MOCK] Wypożyczanie pojazdu...")

def return_vehicle():
    print(">>> [MOCK] Zwracanie pojazdu...")

def remove_vehicle():
    print(">>> [MOCK] Usuwanie pojazdu...")

def pause_vehicle():
    print(">>> [MOCK] Oddanie pojazdu do naprawy...")

def borrow_vehicle_to_client():
    print(">>> [MOCK] Wypozyczenie pojazdu do kientowi...")

def return_vehicle_from_client():
    print(">>> [MOCK] Zwrot pojazdu od kienta...")

def return_vehicle_by_id():
    print(">>> [MOCK] Zwrot pojazdu po ID...")
