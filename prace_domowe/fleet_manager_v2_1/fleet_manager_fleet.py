from fleet_models_db import Vehicle, Car, Scooter, Bike
from sqlalchemy import func, cast, Integer
from sqlalchemy.exc import IntegrityError
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
            print("❌ Wprowadź poprawną liczbę (np. 25.5).")

def add_vehicles_batch():

    # Krok 1. Wybór typu pojazdu
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

        print("\nNiepoprawny typ pojazdu. Spróbuj jeszcze raz")

    count = get_positive_int("\nIle pojazdów chcesz dodać? ")

    # Krok 2. Wprowadzenie wspólnych danych
    print("\n--- Dane wspólne dla całej serii ---")
    brand = input("Producent: ").strip().capitalize()
    model = input("Model: ").strip().capitalize()
    cash_per_day = get_positive_float("Cena za jedną dobę w zł: ")

    specific_fields = {}
    if vehicle_type == "car":
        specific_fields["size"] = input("Rozmiar (Miejski, Kompakt, Limuzyna, Crosover, SUV): ").strip().capitalize()
        specific_fields["fuel_type"] = input("Rodzaj paliwa (benzyna, diesel, hybryda, electric): ").strip()
    elif vehicle_type == "scooter":
        specific_fields["max_speed"] = get_positive_int("prędkość maksymalna (km/h): ")
    elif vehicle_type == "bike":
        specific_fields["bike_type"] = input("Typ roweru (MTB, Miejski, Szosowy): ").strip().capitalize()
        electric_input = input("Czy rower jest elektryczny (tak/nie): ").strip().lower()
        specific_fields["is_electric"] = electric_input in ("tak", "t", "yes", "y")

    # Krok 3. Wprowadzanie indywidualnych i tworzenie pojazdu
    vehicles = []
    with Session() as session:
        for i in range(count):
            print(f"\n--- POJAZD #{i + 1} ---")
            vehicle_id = generate_vehicle_id(session, prefix)
            while True:
                individual_id = input(
                    "Wpisz unikalny identyfikator pojazdu 😊\n"
                    "➡ Dla samochodu i skutera będzie to numer rejestracyjny,\n"
                    "➡ Dla roweru – numer seryjny (zazwyczaj znajdziesz go na ramie, blisko suportu):"
                    "?  "
                ).strip()
                if any(v.individual_id == individual_id for v in vehicles):
                    print("⚠️ Ten identyfikator już istnieje w tej serii. Podaj inny.")
                else:
                    break

            if vehicle_type == "car":
                vehicle = Car(
                    vehicle_id=vehicle_id,
                    brand=brand,
                    vehicle_model=model,
                    cash_per_day=cash_per_day,
                    size=specific_fields["size"],
                    fuel_type=specific_fields["fuel_type"],
                    individual_id=individual_id
                )
            elif vehicle_type == "scooter":
                vehicle = Scooter(
                    vehicle_id=vehicle_id,
                    brand=brand,
                    vehicle_model=model,
                    cash_per_day=cash_per_day,
                    max_speed=specific_fields["max_speed"],

                    individual_id=individual_id
                )
            elif vehicle_type == "bike":
                vehicle = Bike(
                    vehicle_id=vehicle_id,
                    brand=brand,
                    vehicle_model=model,
                    cash_per_day=cash_per_day,
                    bike_type=specific_fields["bike_type"],
                    is_electric=specific_fields["is_electric"],
                    individual_id=individual_id
                )
            session.add(vehicle)
            session.flush()

            vehicles.append(vehicle)

        # Krok 4. Przegląd wpisanych pojazdów
        print("\n--- PRZEGLĄD POJAZDÓW ---")
        for i, v in enumerate(vehicles, 1):
            print(f"\n[{i}] {v}")

        # Krok 5. Czy wszystko się zgadza? Czy poprawić?
        while True:
            answer = input(
                f"\nSprawdź uważnie czy wszystko się zgadza?"
                f"\nWybierz opcję: (Tak/Nie): "
            ).strip().lower()
            if answer in ("tak", "t", "yes", "y"):
                break
            elif answer in ("nie", "n", "no"):
                option = input(
                    f"\nWybierz sposób edycji:"
                    f"\n👉 Numer pojazdu ➡ tylko ten jeden"
                    f"\n👉 'all' ➡ zastosuj zmiany do wszystkich"
                    f"\nPodaj odpowiedź: "
                ).strip().lower()
                if option == "all":
                    print("\n--- Popraw dane wspólne (ENTER = brak zmian) ---")
                    new_brand = input(f"Producent ({brand}): ").strip()
                    new_model = input(f"Model ({model}): ").strip()
                    new_cash = input(f"Cena za dobę ({cash_per_day}): ").strip()
                    if new_brand: brand = new_brand.capitalize()
                    if new_model: model = new_model.capitalize()
                    if new_cash:
                        cash_per_day = get_positive_float("Nowa cena za dobę: ")

                    if vehicle_type == "car":
                        new_size = input(f"Rozmiar ({specific_fields['size']}): ").strip()
                        new_fuel = input(f"Paliwo ({specific_fields["fuel_type"]}): ").strip()
                        if new_size: specific_fields['size'] = new_size.capitalize()
                        if new_fuel: specific_fields['fuel_type'] = new_fuel

                    elif vehicle_type == "scooter":
                        new_speed = input(f"Prędkość maks. ({specific_fields['max_speed']}): ").strip()
                        if new_speed:
                            specific_fields["max_speed"] = get_positive_int("Nowa prędkość maksymalna: ")

                    elif vehicle_type == "bike":
                        new_type = input(f"Typ roweru ({specific_fields['bike_type']})").strip().capitalize()
                        new_electric = input(f"Elektryczny ("
                                            f"{'tak' if specific_fields['is_electric'] else 'nie'}): ").strip().lower()
                        if new_type: specific_fields["bike_type"] = new_type.capitalize()
                        if new_electric:
                            specific_fields["is_electric"] = new_electric in ("tak", "t", "yes", "y")

                    # Krok 6 Aktualizacja wszystkich w serii
                    for v in vehicles:
                        v.brand = brand
                        v.vehicle_model = model
                        v.cash_per_day = cash_per_day
                        for k, val in specific_fields.items():
                            setattr(v, k, val)
                    print("✅ Dane wspólne zostały zaktualizowane.")
                    continue
                elif option.isdigit() and 1 <= int(option) <=len(vehicles):
                    idx = int(option) - 1
                    new_id = input("Nowy identyfikator: ").strip()
                    if any(v.individual_id == new_id for i, v in enumerate(vehicles) if i != idx):
                        print("❌ Taki identyfikator już istnieje.")
                    else:
                        vehicles[idx].individual_id = new_id
                        print("✅ Zmieniono indywidualny identyfikator.")
                        continue
                else:
                    print("🤔 Nie rozumiem, spróbuj jeszcze raz.")
                    continue
            else:
                print("🤔 Wpisz 'tak' lub 'nie'.")

        # Krok 7 Zapis do bazy
        existing_ids = [v.individual_id for v in vehicles]
        if len(existing_ids) != len(set(existing_ids)):
            print("❌ Duplikat identyfikatorów indywidualnych w serii. Operacja przerwana.")
            return

        try:
            for v in vehicles:
                session.add(v)
            session.commit()
            print(f"\n✅ Dodano {len(vehicles)} pojazdów do bazy.")
        except IntegrityError as e:
            session.rollback()
            print(f"\n❌ Błąd zapisu: {e}. Wszystkie zmiany zostały wycofane.")

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