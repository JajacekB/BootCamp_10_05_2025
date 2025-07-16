from fleet_models_db import Vehicle, Car, Scooter, Bike
from sqlalchemy import func, cast, Integer
from fleet_database import Session
from datetime import date, datetime, timedelta
from fleet_models_db import RentalHistory, Invoice

def generate_reservation_id(session):
    last = session.query(RentalHistory).order_by(RentalHistory.id.desc()).first()
    last_num = int(last.reservation_id[1:]) if last else 0
    new_num = last_num + 1
    return f"R{new_num:04d}"

def calculate_rental_cost(user, daily_rate, days, session):
    """
    Zwraca koszt z uwzględnieniem rabatu i programu lojalnościowego.
    """
    # Zlicz zakończone wypożyczenia
    past_rentals = session.query(RentalHistory).filter_by(user_id=user.id).count()
    next_rental_number = past_rentals + 1

    # Lojalność
    if next_rental_number % 10 == 0:
        print("🎉 To Twoje 10. wypożyczenie – za darmo!")
        return 0.0

    # Rabaty
    if days >= 14:
        discount = 0.20
    elif days >= 7:
        discount = 0.09
    elif days >= 5:
        discount = 0.05
    else:
        discount = 0.0

    price = days * daily_rate * (1 - discount)
    if discount > 0:
        print(f"✅ Przyznano rabat {int(discount * 100)}%.")
    return round(price, 2)

def generate_invoice_number(session):
    last = session.query(Invoice).order_by(Invoice.id.desc()).first()
    last_num = int(last.invoice_number.split('-')[-1]) if last else 0
    new_num = last_num + 1
    year = datetime.date.today().year
    return f"F{year}-{new_num:04d}"

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
        vehicle_model = input("\nPodaj model: ").strip().capitalize()
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
            print(f"\nCzy chcesz dodać pojazd?\n{vehicle}")
            choice = input("(Tak/Nie): ").strip().lower()
            if choice in ("tak", "t", "yes", "y"):
                session.add(vehicle)
                session.commit()
                session.refresh(vehicle)
                print(f"\n✅ Pojazd:\n{vehicle}\nzostał dodany pomyślnie.")
                return vehicle
            elif choice in ("nie", "n", "no"):
                print("\nWprowadzanie pojazdu anulowane.")
                return None
            else:
                print("\nNiepoprawna odpowiedź. Wpisz 'tak' lub 'nie'.")

def remove_vehicle():
    vehicle_id = input("\nPodaj numer referencyjny pojazdu, który chcesz usunąć: ").strip().upper()

    with Session() as session:
        vehicle = session.query(Vehicle).filter_by(vehicle_id=vehicle_id).first()

        if not vehicle:
            print("❌ Nie znaleziono pojazdu.")
            return

        if not vehicle.is_available:
            print("🚫 Pojazd jest niedostępny. Nie można go usunąć")
            return

        print(f"\nCzy chcesz usunąć pojad - {vehicle}")
        while True:
            choice = input("\n(Tak/Nie): ").strip().lower()
            if choice in ("tak", "t", "yes", "y"):
                session.delete(vehicle)
                session.commit()
                print("\n✅ Pojazd został usunięty ze stanu wypożyczalni.")
                return
            elif choice in ("nie", "n", "no"):
                print("\n❌ Usuwanie pojazdu anulowane.")
                return
            else:
                print("\n❌ Niepoprawna odpowiedź. spróbuj ponownie.")

def get_vehicle(only_available: bool = False):
    print("\n>>> Przeglądanie pojazdów <<<")

    if only_available:
        status = "available"
    else:
        status = input("\nKtóre pojazdy chcesz przejrzeć (all, available, rented): ").strip().lower()
        if status not in ("all", "available", "rented"):
            print("\n❌ Zły wybór statusu pojazdu, spróbuj jeszcze raz.")
            return

    vehicle_type = input("\nJakiego typu pojazdy chcesz zobaczyć? (all, car, scooter, bike): ").strip().lower()
    if vehicle_type not in ("all", "car", "scooter", "bike"):
        print("\n❌ Zły wybór typu pojazdu, spróbuj jeszcze raz.")
        return

    with Session() as session:
        query = session.query(Vehicle)

        # Filtrowanie po statusie
        if status == "available":
            query = query.filter(Vehicle.is_available == True)
        elif status == "rented":
            query = query.filter(Vehicle.is_available == False)

        # Filtrowanie po typie
        if vehicle_type != "all":
            query = query.filter(Vehicle.type == vehicle_type)

        vehicles = query.order_by(Vehicle.type, Vehicle.vehicle_id).all()

        if not vehicles:
            print("🚫 Brak pojazdów spełniających podane kryteria.")
            return

        current_type = None
        print("\n=== POJAZDY ===")
        for vehicle in vehicles:
            if vehicle.type != current_type:
                current_type = vehicle.type
                print(f"\n--- {current_type.upper()} ---\n")
            print(vehicle, "\n")

def rent_vehicle():
    print(">>> [MOCK] Wypożyczanie pojazdu...")

def return_vehicle():
    print(">>> [MOCK] Zwracanie pojazdu...")

def pause_vehicle():
    print(">>> [MOCK] Oddanie pojazdu do naprawy...")

def rent_vehicle_to_client():
    print(">>> [MOCK] Wypozyczenie pojazdu do kientowi...")

def return_vehicle_from_client():
    print(">>> [MOCK] Zwrot pojazdu od kienta...")

def return_vehicle_by_id():
    print(">>> [MOCK] Zwrot pojazdu po ID...")



# Do użycia przy zwrocie pojazdu.
#
#
# days = (end_date - start_date).days or 1
# total_cost = calculate_rental_cost(user, vehicle.cash_per_day, days, session)
#
# rental = RentalHistory(
#     user_id=user.id,
#     vehicle_id=vehicle.id,
#     start_date=start_date,
#     end_date=end_date,
#     total_cost=total_cost
# )
# session.add(rental)
#
# # Oznacz pojazd jako dostępny
# vehicle.is_available = True
# vehicle.borrower_id = None
# vehicle.return_date = None
#
# session.commit()
# print(f"\n✅ Pojazd zwrócony. Opłata: {total_cost:.2f} zł.")


def create_rental_and_invoice(user, vehicle, start_date, end_date, session):
    days = (end_date - start_date).days or 1
    total_cost = calculate_rental_cost(user, vehicle.cash_per_day, days, session)

    reservation_id = generate_reservation_id(session)
    rental = RentalHistory(
        reservation_id=reservation_id,
        user_id=user.id,
        vehicle_id=vehicle.id,
        start_date=start_date,
        end_date=end_date,
        total_cost=total_cost
    )
    session.add(rental)
    session.flush()  # żeby mieć id rental przed fakturą

    invoice_number = generate_invoice_number(session)
    invoice = Invoice(
        invoice_number=invoice_number,
        rental_id=rental.id,
        amount=total_cost
    )
    session.add(invoice)

    # Aktualizacja statusu pojazdu
    vehicle.is_available = False
    vehicle.borrower_id = user.id
    vehicle.return_date = end_date

    session.commit()

    print(f"\n✅ Rezerwacja {reservation_id} została utworzona.")
    print(f"📄 Faktura numer: {invoice_number}, kwota: {total_cost} zł.")
    return rental, invoice