from fleet_models_db import Vehicle, Car, Scooter, Bike, User, RentalHistory, Invoice, Promotion, RepairHistory
from sqlalchemy import func, cast, Integer, extract, and_, or_, exists, select
from sqlalchemy.exc import IntegrityError
from fleet_database import Session, SessionLocal
from datetime import date, datetime, timedelta
from collections import defaultdict
from fleet_manager_user import get_users_by_role
from fleet_utils_db import (
    get_positive_int, get_positive_float,generate_repair_id,
    generate_vehicle_id, generate_reservation_id, generate_invoice_number,
    calculate_rental_cost, get_available_vehicles, get_vehicles_unavailable_today
)

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
            vehicle_id = generate_vehicle_id(prefix, session)
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
                        new_fuel = input(f"Paliwo ({specific_fields['fuel_type']}): ").strip()
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
            session.flush()
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
        while True:
            status = input("\nKtóre pojazdy chcesz przejrzeć (all, available, rented): ").strip().lower()
            if status in ("all", "available", "rented"):
                break
            print("\n❌ Zły wybór statusu pojazdu, spróbuj jeszcze raz.")

    while True:
        vehicle_type = input("\nJakiego typu pojazdy chcesz zobaczyć? (all, car, scooter, bike): ").strip().lower()
        if vehicle_type in ("all", "car", "scooter", "bike"):
            break
        print("\n❌ Zły wybór typu pojazdu, spróbuj jeszcze raz.")

    with Session() as session:
        if status == "available":
            vehicles = get_available_vehicles(session)
        elif status == "rented":
            unavailable_ids = get_vehicles_unavailable_today(session)
            if not unavailable_ids:
                print("\n🚫 Brak niedostępnych pojazdów na dziś.")
                return
            vehicles = session.query(Vehicle).filter(Vehicle.id.in_(unavailable_ids)).all()
        else:
            vehicles = session.query(Vehicle).all()

        if vehicle_type != "all":
            vehicles = [v for v in vehicles if v.type == vehicle_type]

        if not vehicles:
            print("🚫 Brak pojazdów spełniających podane kryteria.")
            return

        # Przygotowujemy gotowe stringi WEWNĄTRZ sesji
        output_lines = []
        current_type = None
        for vehicle in sorted(vehicles, key=lambda v: (v.type, v.vehicle_id)):
            if vehicle.type != current_type:
                current_type = vehicle.type
                output_lines.append(f"\n--- {current_type.upper()} ---\n")
            output_lines.append(str(vehicle) + "\n")

    # Po wyjściu z with sesja jest zamknięta,
    # ale mamy już gotowe teksty do wyświetlenia
    print("\n=== POJAZDY ===")
    for line in output_lines:
        print(line)


def rent_vehicle_for_client(user: User):
    print(f"\n>>> Rezerwacja dla klienta <<<")

    if user.role.lower() not in ("seller", "admin"):
        print("🚫 Tylko sprzedawcy i administratorzy mogą rezerwować pojazdy dla klientów.")
        return

    with Session() as session:
        while True:
            client_id = get_positive_int(
                "\nPodaj id klienta, dla którego chcesz wynająć pojazd (ENTER = Ty sam): ",
                allow_empty=True
            )

            if client_id is None:
                print(f"\nWypożyczasz pojazd dla siebie: {user.first_name} {user.last_name} ({user.login}).")
                rent_vehicle(user)
                return


            client = session.query(User).filter_by(id=client_id).first()
            if not client:
                print("❌ Nie znaleziono użytkownika o podanym ID.")
                continue

            print(f"\nZnaleziony klient: {client.id}, rola: '{client.role}'")  # diagnostyka

            if client.role.lower() != "client":
                print("🚫 Ten użytkownik nie ma roli klienta.")
                continue

            print(f"\nWypozyczasz pojazd dla: [{client.id}] - {client.first_name} {client.last_name}.")

            rent_vehicle(client, session=session)
            return


def rent_vehicle(user: User, session=None):
    if session is None:
        with Session() as session:
            return rent_vehicle(user, session=session)

    print("\n=== WYPOŻYCZENIE POJAZDU ===\n")
    vehicle_type = input("Wybierz typ pojazdu (bike, car, scooter): ").strip().lower()
    start_date_str = input("\nData rozpoczęcia (DD-MM-YYYY): ").strip()
    end_date_str = input("Data zakończenia (DD-MM-YYYY): ").strip()

    try:
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()
        planned_return_date = datetime.strptime(end_date_str, "%d-%m-%Y").date()
    except ValueError:
        print("❌ Niepoprawny format daty.")
        return

    # Krok 1: Znajdź dostępne pojazdy
    available_vehicles = (
        session.query(Vehicle)
        .filter(Vehicle.type == vehicle_type)
        .filter(~Vehicle.rental_history.any(
            (RentalHistory.start_date <= planned_return_date) &
            (RentalHistory.planned_return_date >= start_date)
        ))
        .filter(Vehicle.is_available == True)
        .order_by(Vehicle.cash_per_day, Vehicle.brand, Vehicle.vehicle_model)
        .all()
    )

    if not available_vehicles:
        print("\n🚫 Brak dostępnych pojazdów w tym okresie.")
        return

    # Krok 2: Grupuj pojazdy
    grouped = defaultdict(list)
    for v in available_vehicles:
        key = (v.brand, v.vehicle_model, v.cash_per_day)
        grouped[key].append(v)

    print("\nDostępne grupy pojazdów:\n")
    for (brand, model, price), vehicles in grouped.items():
        print(f"{brand} | {model} | {price} zł/dzień | Dostępnych: {len(vehicles)}")

    # Krok 3: Wybór modelu
    while True:
        chosen_model = input("\nPodaj model pojazdu do wypożyczenia: ").strip()
        chosen_vehicle = next(
            (v for v in available_vehicles if v.vehicle_model.lower() == chosen_model.lower()),
            None
        )

        if not chosen_vehicle:
            print("🚫 Nie znaleziono pojazdu o podanym modelu. Wybierz ponownie.")
        else:
            break

    # Krok 4: Oblicz koszty i rabaty
    days = (planned_return_date - start_date).days
    base_cost = days * chosen_vehicle.cash_per_day
    total_cost, discount_value, discount_type = calculate_rental_cost(
        user, chosen_vehicle.cash_per_day, days
    )

    # Krok 5: Potwierdzenie
    print(f"\nKoszt podstawowy: {base_cost} zł")
    confirm = input(
        f"Całkowity koszt wypożyczenia po rabatach: {total_cost:.2f} zł.\n"
        f"Czy potwierdzasz? (Tak/Nie): "
    ).strip().lower()
    if confirm not in ("tak", "t", "yes", "y"):
        print("\n🚫 Anulowano rezerwację.")
        return

    # Krok 6: Zapis danych do bazy
    reservation_id = generate_reservation_id()
    invoice_number = generate_invoice_number(planned_return_date)

    # Aktualizacja pojazdu
    chosen_vehicle.is_available = False
    chosen_vehicle.borrower_id = user.id
    session.add(chosen_vehicle)

    # Historia wypożyczeń
    rental = RentalHistory(
        reservation_id=reservation_id,
        user_id=user.id,
        vehicle_id=chosen_vehicle.id,
        start_date=start_date,
        planned_return_date=planned_return_date,
        base_cost=base_cost,
        total_cost=total_cost
    )

    # Faktura
    invoice = Invoice(
        invoice_number=invoice_number,
        rental_id=reservation_id,
        amount=total_cost,
        issue_date=planned_return_date
    )

    session.add_all([rental, invoice])
    session.commit()

    print(
        f"\n✅ Zarezerwowałeś {chosen_vehicle.brand} {chosen_vehicle.vehicle_model} "
        f"od {start_date} do {planned_return_date}.\nMiłej jazdy!"
    )


def return_vehicle(user: User):
    with Session() as session:

        def update_costs_and_invoice(rental, vehicle, actual_return_date):
            #from fleet_utils_db import calculate_discounted_cost  # funkcja uwzględniająca rabaty
            from datetime import date

            start_date = rental.start_date
            planned_return = rental.planned_return_date
            planned_days = (planned_return - start_date).days + 1

            rental.actual_return_date = actual_return_date
            rental_days = (actual_return_date - start_date).days + 1
            if rental_days < 1:
                rental_days = 1

            if actual_return_date < planned_return:
                # Zwrot wcześniej
                base_cost = calculate_rental_cost(vehicle.cash_per_day, rental_days)
                late_fee = 0
                print(f"Zwrot wcześniej – nowy koszt na {rental_days} dni: {base_cost:.2f} zł")

            elif actual_return_date > planned_return:
                # Zwrot po terminie
                base_cost = calculate_rental_cost(vehicle.cash_per_day, planned_days)
                delay_days = (actual_return_date - planned_return).days
                late_fee = delay_days * vehicle.cash_per_day
                print(f"Zwrot po terminie o {delay_days} dni. Kara: {late_fee:.2f} zł")

            else:
                # Zwrot w terminie
                actual_return_date = planned_return
                rental.actual_return_date = actual_return_date
                base_cost = calculate_rental_cost(vehicle.cash_per_day, planned_days)
                late_fee = 0
                print(f"Zwrot w terminie. Koszt: {base_cost:.2f} zł")

            total_cost = base_cost + late_fee
            rental.total_cost = total_cost

            # Aktualizacja faktury
            if rental.invoice:
                rental.invoice.amount = total_cost
                rental.invoice.issue_date = actual_return_date

            # Aktualizacja pojazdu
            vehicle.is_available = True
            vehicle.borrower_id = None
            vehicle.return_date = None

        def process_return_for_vehicle(vehicle):

            # Znajdź aktywne wypożyczenie (związane z pojazdem i użytkownikiem)
            rental = session.query(RentalHistory).filter_by(
                vehicle_id=vehicle.id,
                user_id=vehicle.borrower_id
            ).order_by(RentalHistory.start_date.desc()).first()

            if not rental:
                print(f"Nie znaleziono historii wypożyczenia pojazdu {vehicle.vehicle_model}. Pomijam.")
                return False

            print(f"\nPojazd do zwrotu: {vehicle.brand} {vehicle.vehicle_model} (ID: {vehicle.vehicle_id})")
            print(f"Planowany termin zwrotu: {rental.planned_return_date}")

            actual_return_str = input("Podaj datę faktycznego zwrotu (DD-MM-YYYY): ").strip()
            try:
                actual_return_date = datetime.strptime(actual_return_str, "%d-%m-%Y").date()
            except ValueError:
                print("Niepoprawny format daty. Zwrot pominięty.")
                return False

            update_costs_and_invoice(rental, vehicle, actual_return_date)

            # Aktualizacja pojazdu - zwrot
            vehicle.is_available = True
            vehicle.borrower_id = None
            vehicle.return_date = None

            session.commit()
            print(f"Pojazd {vehicle.vehicle_model} został zwrócony i jest dostępny.")
            return True

        if user.role == "client":
            # Pobierz pojazdy wypożyczone przez klienta
            rented_vehicles = session.query(Vehicle).filter(
                Vehicle.borrower_id == user.id,
                Vehicle.is_available == False
            ).all()

            if not rented_vehicles:
                print("Nie masz obecnie wypożyczonych pojazdów.")
                return

            for vehicle in rented_vehicles:
                print("\nCzy chcesz zwrócić ten pojazd?")
                print(f"{vehicle.brand} {vehicle.vehicle_model} (ID: {vehicle.vehicle_id})")
                answer = input("(tak/nie): ").strip().lower()
                if answer not in ("tak", "t", "yes", "y"):
                    continue
                process_return_for_vehicle(vehicle)

        elif user.role in ("seller", "admin"):
            while True:
                # Najpierw opcjonalnie wyświetl wypożyczone pojazdy dla danego użytkownika - albo od razu pytaj o ID pojazdu
                vehicle_id_str = input("\nPodaj ID pojazdu do zwrotu (lub wpisz 'koniec' aby wyjść): ").strip()
                if vehicle_id_str.lower() == "koniec":
                    break

                try:
                    vehicle_id = int(vehicle_id_str)
                except ValueError:
                    print("Niepoprawne ID pojazdu.")
                    continue

                vehicle = session.query(Vehicle).filter_by(id=vehicle_id).first()
                if not vehicle:
                    print("Nie znaleziono pojazdu o podanym ID.")
                    continue

                if vehicle.is_available:
                    print("Ten pojazd jest już dostępny, nie jest wypożyczony.")
                    continue

                process_return_for_vehicle(vehicle)

        else:
            print("Funkcja dostępna tylko dla klientów, sprzedawców i administratorów.")

def repair_vehicle():
    with SessionLocal() as session:
        available_vehicles = get_available_vehicles()
        if not available_vehicles:
            print("Brak dostępnych pojazdów do naprawy.")
            return

        print("\nDostępne pojazdy do naprawy:")
        for v in available_vehicles:
            print(f"- {v.vehicle_model} ({v.type}), ID: {v.id}, Numer: {v.individual_id}")

        try:
            vehicle_id = int(input("Podaj ID pojazdu do przekazania do naprawy: "))
        except ValueError:
            print("Błędne ID.")
            return

        vehicle = session.query(Vehicle).filter_by(id=vehicle_id, is_available=True).first()
        if not vehicle:
            print("Nie znaleziono pojazdu lub jest niedostępny.")
            return

        workshops = get_users_by_role("workshop", session)
        if not workshops:
            print("Brak zdefiniowanych użytkowników warsztatu.")
            return

        print("\nDostępne warsztaty:")
        for idx, w in enumerate(workshops, 1):
            print(f"{idx}. {w.first_name} {w.last_name} ({w.login})")

        workshop_choice = get_positive_int("Wybierz numer warsztatu: ") - 1
        selected_workshop = workshops[workshop_choice]

        repair_days = get_positive_int("Podaj liczbę dni naprawy: ")
        planed_return_date = datetime.today().date() + timedelta(days=repair_days)

        repair_cost_per_day = get_positive_float("\nPodaj jednostkowy koszt naprawy: ")
        repair_cost = repair_cost_per_day * repair_days

        description = input("\nKrótko opisz zakres naprawy: ")

        while True:
            confirm = input(
                f"\nPotwierdź oddanie do naprawy pojazdu:\n {vehicle}"
                f"\nKoszt naprawy {repair_cost} zł"
                f"\nWybierz (tak/nie): "
            ).strip().lower()
            if confirm not in ("tak", "t", "yes", "y"):
                print("\nNaprawa anulowana.")
                return

            # Historia naprawy
            repair_id = generate_repair_id()

            repair = RepairHistory(
                repair_id=repair_id,
                vehicle_id=vehicle.id,
                mechanic_id=selected_workshop.id,
                start_date=datetime.today().date(),
                planed_return_date=planed_return_date,
                actual_return_date=None,  # Domyślnie brak
                cost=repair_cost,
                description=description
            )
            session.add(repair)

            # Aktualizacja pojazdu
            vehicle.is_available = False
            vehicle.borrower_id = selected_workshop.id
            vehicle.return_date = planed_return_date  # Jeśli jeszcze używasz tej kolumny w Vehicle

            session.commit()
            print(
                f"\nPojazd {vehicle.brand} {vehicle.vehicle_model} {vehicle.individual_id}"
                f"\nprzekazany do warsztatu: {selected_workshop.first_name} {selected_workshop.last_name} do dnia {planed_return_date}."
            )
            return