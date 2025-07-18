from datetime import datetime, date
from collections import defaultdict
from uuid import uuid4
from sqlalchemy.orm import Session
from fleet_models_db import Vehicle, RentalHistory, Invoice, User


def rent_vehicle(session: Session, user: User):
    print("=== WYPOŻYCZENIE POJAZDU ===")
    vehicle_type = input("Wybierz typ pojazdu (car, bike, scooter): ").lower()
    start_date_str = input("Data rozpoczęcia (YYYY-MM-DD): ")
    end_date_str = input("Data zakończenia (YYYY-MM-DD): ")

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    # Krok 1: Znajdź dostępne pojazdy
    available_vehicles = (
        session.query(Vehicle)
        .filter(Vehicle.type == vehicle_type)
        .filter(~Vehicle.rental_history.any(
            (RentalHistory.start_date <= end_date) &
            (RentalHistory.end_date >= start_date)
        ))
        .filter(Vehicle.is_available == True)
        .all()
    )

    if not available_vehicles:
        print("Brak dostępnych pojazdów w tym okresie.")
        return

    # Krok 2: Grupuj pojazdy
    grouped = defaultdict(list)
    for v in available_vehicles:
        key = (v.vehicle_model, v.cash_per_day)
        grouped[key].append(v)

    print("Dostępne grupy pojazdów:")
    for (model, price), vehicles in grouped.items():
        print(f"{model} | {price} zł/dzień | Dostępnych: {len(vehicles)}")

    # Krok 3: Wybór modelu
    chosen_model = input("Podaj model pojazdu do wypożyczenia: ")
    chosen_vehicle = next(
        (v for v in available_vehicles if v.vehicle_model == chosen_model),
        None
    )

    if not chosen_vehicle:
        print("Nie znaleziono pojazdu o podanym modelu.")
        return

    # Krok 4: Oblicz koszt i rabat
    days = (end_date - start_date).days
    base_cost = days * chosen_vehicle.cash_per_day

    discount = 0
    if days >= 14:
        discount = 0.20
    elif days >= 7:
        discount = 0.10

    total_cost = round(base_cost * (1 - discount), 2)

    print(f"Koszt podstawowy: {base_cost} zł")
    print(f"Rabat: {int(discount * 100)}%")
    print(f"Do zapłaty: {total_cost} zł")

    confirm = input("Czy potwierdzasz rezerwację? (tak/nie): ")
    if confirm.lower() != 'tak':
        print("Anulowano rezerwację.")
        return

    # Krok 5: Zapisz dane
    reservation_id = str(uuid4())

    # Aktualizacja pojazdu
    chosen_vehicle.is_available = False
    chosen_vehicle.return_date = end_date
    chosen_vehicle.borrower_id = user.id

    # Historia wypożyczenia
    rental = RentalHistory(
        reservation_id=reservation_id,
        user_id=user.id,
        vehicle_id=chosen_vehicle.id,
        start_date=start_date,
        end_date=end_date,
        total_cost=total_cost
    )

    # Faktura
    invoice = Invoice(
        reservation_id=reservation_id,
        user_id=user.id,
        amount=total_cost,
        date_issued=date.today()
    )

    session.add_all([rental, invoice])
    session.commit()

    print("Wypożyczenie zakończone sukcesem!")
