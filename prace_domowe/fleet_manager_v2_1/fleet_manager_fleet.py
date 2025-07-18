from fleet_models_db import Vehicle, Car, Scooter, Bike, User, RentalHistory, Invoice, Promotion
from sqlalchemy import func, cast, Integer, extract, and_, or_, exists, select
from sqlalchemy.exc import IntegrityError
from fleet_database import Session, SessionLocal
from datetime import date, datetime, timedelta
from collections import defaultdict
from fleet_manager_user import get_clients, get_users_by_role


def generate_reservation_id():
    with Session() as session:
        last = session.query(RentalHistory).order_by(RentalHistory.id.desc()).first()
        last_num = int(last.reservation_id[1:]) if last else 0
        new_num = last_num + 1
        return f"R{new_num:04d}"

def calculate_rental_cost(user, daily_rate, days):
    with Session() as session:
        """
        Zwraca koszt z uwzględnieniem rabatu czasowego i lojalnościowego.
        """
        # Zlicz zakończone wypożyczenia
        past_rentals = session.query(RentalHistory).filter_by(user_id=user.id).count()
        next_rental_number = past_rentals + 1

        # Sprawdzenie promocji lojalnościowej (co 10. wypożyczenie)
        loyalty_discount_days = 1 if next_rental_number % 10 == 0 else 0
        if loyalty_discount_days == 1:
            print("🎉 To Twoje 10., 20., 30... wypożyczenie – pierwszy dzień za darmo!")

        # Pobierz rabaty czasowe z tabeli
        time_promos = session.query(Promotion).filter_by(type="time").order_by(Promotion.min_days.desc()).all()

        discount = 0.0
        for promo in time_promos:
            if days >= promo.min_days:
                discount = promo.discount_percent / 100.0
                print(f"\n✅ Przyznano rabat {int(promo.discount_percent)}% ({promo.description})")
                break

        # Cena po uwzględnieniu rabatu i 1 dnia gratis (jeśli przysługuje)
        paid_days = max(days - loyalty_discount_days, 0)
        price = paid_days * daily_rate * (1 - discount)

        return round(price, 2), discount * 100, "lojalność + czasowy" if discount > 0 and loyalty_discount_days else (
            "lojalność" if loyalty_discount_days else (
            "czasowy" if discount > 0 else "brak"))

def generate_invoice_number(end_date):
    """
                Generuje numer faktury w formacie FV/YYYY/MM/NNNN
                - session: aktywna sesja SQLAlchemy
                - end_date: data zakończenia wypożyczenia (datetime.date)
                """
    with Session() as session:

        year = end_date.year
        month = end_date.month

        # Policz faktury wystawione w danym roku i miesiącu
        count = session.query(Invoice).filter(
            extract('year', Invoice.issue_date) == year,
            extract('month', Invoice.issue_date) == month
        ).count()

        # Dodaj 1 do sekwencji
        sequence = count + 1

        # Zbuduj numer faktury
        invoice_number = f"FV/{year}/{month:02d}/{sequence:04d}"
        return invoice_number

def generate_vehicle_id( prefix: str) -> str:
    with Session() as session:
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

def get_positive_int(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if allow_empty and not value:
            return None
        try:
            value = int(value)
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
            vehicle_id = generate_vehicle_id(prefix)
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

    today = date.today()

    with Session() as session:

        # Podstawowe zapytanie - LEFT OUTER JOIN z RentalHistory
        active_rental_subq = session.query(RentalHistory.id).filter(
            RentalHistory.vehicle_id == Vehicle.id,
            RentalHistory.start_date <= today,
            RentalHistory.end_date >= today
        ).exists()

        query = session.query(Vehicle)

        # Filtrowanie po typie pojazdu
        if vehicle_type != "all":
            query = query.filter(Vehicle.type == vehicle_type)

        # Filtrujemy po statusie
        if status == "available":
            # Pojazdy bez aktywnego wynajmu na dziś i z is_available = True
            query = query.filter(
                and_(
                    ~active_rental_subq,
                    Vehicle.is_available == True
                )
            )
        elif status == "rented":
            # Pojazdy które mają aktywny wynajem na dziś lub is_available=False
            query = query.filter(
                or_(
                    active_rental_subq,
                    Vehicle.is_available == False
                )
            )
        # status == "all" - bez dodatkowych filtrów

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

def rent_vehicle(user: User):
    print("\n=== WYPOŻYCZENIE POJAZDU ===\n")
    vehicle_type = input("Wybierz typ pojazdu (bike, car, scooter): ").strip().lower()
    start_date_str = input("\nData rozpoczęcia (DD-MM-YYYY): ").strip()
    end_date_str = input("Data zakończenia (DD-MM-YYYY): ").strip()

    start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()
    end_date = datetime.strptime(end_date_str, "%d-%m-%Y").date()

    # Krok 1: Znajdź dostępne pojazdy
    with Session() as session:
        available_vehicles = (
            session.query(Vehicle)
            .filter(Vehicle.type == vehicle_type)
            .filter(~Vehicle.rental_history.any(
                (RentalHistory.start_date <= end_date) &
                (RentalHistory.end_date >= start_date)
            ))
            .filter(Vehicle.is_available == True)
            .order_by(Vehicle.cash_per_day, Vehicle.brand, Vehicle.vehicle_model)
            .all()
        )

        if not available_vehicles:
            print("|\n🚫 Brak dostępnych pojazdów w tym okresie.")
            return

        # Krok 2: Grupuj pojazdy
        grouped = defaultdict(list)
        for v in available_vehicles:
            key = (v.brand, v.vehicle_model, v.cash_per_day)
            grouped[key].append(v)

        print("\n Dostępne grupy pojazdów:\n")
        for (brand, model, price), vehicles in grouped.items():
            print(f"{brand} | {model} | {price} zł/dzień | Dostępnych: {len(vehicles)}")

        # Krok 3: Wybór modelu
        while True:
            choosen_model = input("\nPodaj model pojazdu do wypożyczenia: ").strip()
            choosen_vehicle = next(
                (v for v in available_vehicles if v.vehicle_model.lower() == choosen_model.lower()),
                None
            )

            if not choosen_vehicle:
                print("\n🚫 Nie znaleziono pojazdu o podanym medelu. Wybierz ponownie")
                continue

            else:
                break

        # Krok 4: Oblicz koszty i rabaty.
        days = (end_date - start_date).days
        base_cost = days * choosen_vehicle.cash_per_day
        total_cost, discount_value, discount_type = calculate_rental_cost(user, choosen_vehicle.cash_per_day, days)

        # Krok 5. Potwierdzenie

        print(f"\nKoszt podstawowy: {base_cost} zł")
        confirm = input(
            f"\nCałkowity koszt wypozyczenia po naliczeniu rabatów to: {total_cost:.2f} zł.\n"
            f"Czy akceptujesz? (Tak/Nie): "
        ).strip().lower()
        if confirm not in ("tak", "t", "yes", "y"):
            print("\n🚫 Anulowano rezerwację")
            return

        # Krok 6. Zapis danych do bazy

        # Generowanie numerów do rezerwacji i faktury
        reservation_id = generate_reservation_id()
        invoice_number = generate_invoice_number(end_date)

        # Aktualizowanie wypożyczonego pojazdu
        choosen_vehicle.is_available = False
        choosen_vehicle.return_date = end_date
        choosen_vehicle.borrower_id = user.id

        session.add(choosen_vehicle)

        # Aktualizacja historii wypożyczeń
        rental = RentalHistory(
            reservation_id=reservation_id,
            user_id=user.id,
            vehicle_id=choosen_vehicle.id,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost
        )

        # Dane do faktury
        invoice = Invoice(
            invoice_number=invoice_number,
            rental_id=reservation_id,
            amount=total_cost,
            issue_date=end_date
        )

        session.add_all([rental, invoice])
        session.commit()

        print(
            f"\n✅ Zarezerwowałeś {choosen_vehicle.brand} {choosen_vehicle.vehicle_model}\n"
            f"W terminie od {start_date} do {end_date}.\n"
            f" Miłej jazdy!")

def rent_vehicle_for_client(user: User):
    print(f"\n>>> Rezerwacja dla klienta <<<")
    while True:
        client_id = get_positive_int(
            "\nPodaj id klienta, dla którego chcesz wynająć pojazd (ENTER = Ty sam): ",
            allow_empty=True
        )

        if client_id is None:
            print(f"\nWypozyczasz pojazd dla: {client.login}.")
            rent_vehicle(user)
            return

        with Session() as session:
            client = session.query(User).filter_by(id=client_id).first()
            if not client:
                print("❌ Nie znaleziono użytkownika o podanym ID.")
                continue

            print(f"\nZnaleziony klient: {client.id}, rola: '{client.role}'")  # diagnostyka

            if client.role.lower() != "client":
                print("🚫 Ten użytkownik nie ma roli klienta.")
                continue

            print(f"\nWypozyczasz pojazd dla: [{client.id}] - {client.first_name} {client.last_name}.")

            rent_vehicle(client)
            return

def check_overdue_vehicles(user, session):
    if user.role not in ("seller", "admin"):
        return  # tylko dla seller i admin

    print("\n=== Sprawdzanie przeterminowanych zwrotów pojazdów ===")

    today = date.today()
    overdue_vehicles = session.query(Vehicle).filter(
        Vehicle.return_date != None,
        Vehicle.return_date < today,
        Vehicle.is_available == False
    ).order_by(Vehicle.return_date.asc()).all()

    if not overdue_vehicles:
        print("Brak przeterminowanych zwrotów.\n")
        return

    for vehicle in overdue_vehicles:
        print(f"\nPojazd: {vehicle.brand} {vehicle.vehicle_model} (ID: {vehicle.vehicle_id})")
        print(f"Planowany zwrot: {vehicle.return_date}")
        answer = input("Czy pojazd został zwrócony? (tak/nie): ").strip().lower()

        if answer in ("tak", "t", "yes", "y"):
            actual_return_str = input("Podaj datę zwrotu (DD-MM-YYYY): ").strip()
            try:
                actual_return_date = datetime.strptime(actual_return_str, "%d-%m-%Y").date()
            except ValueError:
                print("Niepoprawny format daty, pomijam ten pojazd.")
                continue

            # Oblicz opóźnienie
            delay_days = (actual_return_date - vehicle.return_date).days
            delay_days = max(0, delay_days)

            # Szukamy powiązanej historii wypożyczenia (ostatniej rezerwacji tego pojazdu i tego wypożyczającego)
            rental = session.query(RentalHistory).filter_by(
                vehicle_id=vehicle.id,
                user_id=vehicle.borrower_id
            ).order_by(RentalHistory.end_date.desc()).first()

            if not rental:
                print("Nie znaleziono historii wypożyczenia tego pojazdu dla tego użytkownika.")
                continue

            # Obliczamy dodatkową opłatę za opóźnienie (100% ceny za dzień)
            additional_fee = delay_days * vehicle.cash_per_day
            print(f"Dodatkowa opłata za {delay_days} dni opóźnienia: {additional_fee:.2f} zł")

            # Aktualizujemy end_date w RentalHistory (przedłużenie wypożyczenia)
            if actual_return_date > rental.end_date:
                print(f"Przedłużam wypożyczenie z {rental.end_date} do {actual_return_date}")
                rental.end_date = actual_return_date

                # Aktualizujemy całkowity koszt (bez rabatów, bo to dodatkowe dni)
                base_days = (rental.end_date - rental.start_date).days + 1  # liczymy dni od początku do nowej daty
                new_total_cost = base_days * vehicle.cash_per_day
                rental.total_cost = new_total_cost

                # Aktualizujemy fakturę powiązaną z rezerwacją (Invoice)
                invoice = rental.invoice
                if invoice:
                    invoice.amount = new_total_cost
                    print(f"Zaktualizowano kwotę faktury do: {invoice.amount:.2f} zł")
                else:
                    print("Brak faktury powiązanej z tą rezerwacją, nie można zaktualizować kwoty.")

            # Aktualizacja pojazdu - zwrot i czyszczenie danych
            vehicle.is_available = True
            vehicle.borrower_id = None
            vehicle.return_date = None

            session.commit()
            print(f"Pojazd {vehicle.vehicle_model} został zwrócony i jest dostępny.")

        else:
            print("Pojazd nadal wypożyczony, sprawdzimy go ponownie jutro.")

    print("\n=== Koniec sprawdzania przeterminowanych zwrotów ===\n")

def return_vehicle(user):
    with Session() as session:

        def update_costs_and_invoice(rental, vehicle, actual_return_date):
            # Oblicz liczbę dni wynajmu od startu do faktycznego zwrotu
            rental_days = (actual_return_date - rental.start_date).days + 1
            if rental_days < 1:
                rental_days = 1  # minimum 1 dzień

            planned_days = (rental.end_date - rental.start_date).days + 1

            # Czy zwrot jest przed terminem?
            if actual_return_date < rental.end_date:
                # Skrócenie wypożyczenia - zmniejszamy koszt i anulujemy rabaty
                rental.end_date = actual_return_date
                rental.total_cost = rental_days * vehicle.cash_per_day  # bez rabatów
                print(f"Zwrot przed terminem. Nowa kwota do zapłaty: {rental.total_cost:.2f} zł (brak rabatów)")
            elif actual_return_date > rental.end_date:
                # Przeterminowanie - doliczamy opłatę 100% ceny za każdy dzień opóźnienia
                delay_days = (actual_return_date - rental.end_date).days
                base_cost = planned_days * vehicle.cash_per_day
                additional_fee = delay_days * vehicle.cash_per_day
                rental.end_date = actual_return_date
                rental.total_cost = base_cost + additional_fee
                print(f"Przeterminowanie o {delay_days} dni. Kwota do zapłaty: {rental.total_cost:.2f} zł (w tym opłata za opóźnienie {additional_fee:.2f} zł)")
            else:
                # Zwrot dokładnie w terminie
                rental.total_cost = planned_days * vehicle.cash_per_day
                print(f"Zwrot w terminie. Kwota do zapłaty: {rental.total_cost:.2f} zł")

            # Aktualizuj fakturę powiązaną z wypożyczeniem
            if rental.invoice:
                rental.invoice.amount = rental.total_cost
                print(f"Zaktualizowano fakturę: {rental.invoice.invoice_number}, kwota: {rental.invoice.amount:.2f} zł")

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
            print(f"Planowany termin zwrotu: {rental.end_date}")

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

def get_available_vehicles(session):
    today = date.today()

    # Krok 1: Wszystkie pojazdy oznaczone jako dostępne
    available_vehicles = session.query(Vehicle).filter(Vehicle.is_available == True).all()

    truly_available = []
    for vehicle in available_vehicles:
        # Krok 2: Sprawdzenie czy pojazd nie ma aktywnego wypożyczenia na dzisiaj
        active_rental = session.query(RentalHistory).filter(
            RentalHistory.vehicle_id == vehicle.vehicle_id,
            RentalHistory.start_date <= today,
            RentalHistory.end_date >= today
        ).first()

        if not active_rental:
            truly_available.append(vehicle)

    return truly_available


def repair_vehicle():
    with SessionLocal() as session:
        available_vehicles = get_available_vehicles(session)
        if not available_vehicles:
            print("Brak dostępnych pojazdów do naprawy.")
            return

        print("\nDostępne pojazdy do naprawy:")
        for v in available_vehicles:
            print(f"- {v.vehicle_model} ({v.vehicle_type}), ID: {v.id}, Numer: {v.individual_id}")

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

        try:
            workshop_choice = int(input("Wybierz numer warsztatu: ")) - 1
            selected_workshop = workshops[workshop_choice]
        except (IndexError, ValueError):
            print("Nieprawidłowy wybór.")
            return

        try:
            repair_days = int(input("Podaj liczbę dni naprawy: "))
            return_date = datetime.today().date() + timedelta(days=repair_days)
        except ValueError:
            print("Błędna liczba dni.")
            return

        # Historia naprawy
        history = RentalHistory(
            user_id=selected_workshop.id,
            vehicle_id=vehicle.id,
            rent_date=datetime.today().date(),
            return_date=return_date,
            repair=True  # jeśli masz taką kolumnę; jeśli nie — usuń
        )
        session.add(history)

        # Aktualizacja pojazdu
        vehicle.is_available = False
        vehicle.borrower_id = selected_workshop.id
        vehicle.return_date = return_date

        session.commit()
        print(f"\nPojazd {vehicle.vehicle_model} przekazany do warsztatu: {selected_workshop.first_name} {selected_workshop.last_name} do dnia {return_date}.")

