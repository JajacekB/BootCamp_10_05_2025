from fleet_models_db import Vehicle, Car, Scooter, Bike, User, RentalHistory, Invoice, Promotion, RepairHistory
from fleet_database import Session, SessionLocal
from sqlalchemy import func, cast, Integer, extract, and_, or_, exists, select
from datetime import datetime, date


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

def generate_reservation_id():
    with Session() as session:
        last = session.query(RentalHistory).order_by(RentalHistory.id.desc()).first()
        if last and last.reservation_id and len(last.reservation_id) > 1 and last.reservation_id[1:].isdigit():
            last_num = int(last.reservation_id[1:])
        else:
            last_num = 0
        new_num = last_num + 1

        # Określamy długość cyfr - minimalnie 4, albo więcej jeśli liczba jest większa
        digits = max(4, len(str(new_num)))
        return f"R{new_num:0{digits}d}"

def generate_repair_id():
    with Session() as session:
        last = session.query(RepairHistory).order_by(RepairHistory.id.desc()).first()
        if last and last.repair_id and len(last.repair_id) > 1 and last.repair_id[1:].isdigit():
            last_num = int(last.repair_id[1:])
        else:
            last_num = 0
        new_num = last_num + 1

        # Określamy długość cyfr - minimalnie 4, albo więcej jeśli liczba jest większa
        digits = max(4, len(str(new_num)))
        return f"N{new_num:0{digits}d}"

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

def get_available_vehicles():
    with Session() as session:
        today = date.today()

        # Krok 1: Wszystkie pojazdy oznaczone jako dostępne
        available_vehicles = session.query(Vehicle).filter(Vehicle.is_available == True).all()

        truly_available = []
        for vehicle in available_vehicles:
            # Krok 2: Sprawdzenie czy pojazd nie ma aktywnego wypożyczenia na dzisiaj
            active_rental = session.query(RentalHistory).filter(
                and_(
                    RentalHistory.vehicle_id == vehicle.vehicle_id,
                    RentalHistory.start_date <= today,
                    RentalHistory.end_date >= today
                )
            ).first()

            active_repair = session.query(RepairHistory).filter(
                and_(
                    RepairHistory.vehicle_id == vehicle.vehicle_id,
                    RepairHistory.start_date <= today,
                    RepairHistory.end_date >= today
                    )
            ).first()

            if not active_rental and not active_repair:
                truly_available.append(vehicle)

        return truly_available

def get_vehicles_unavailable_today():
    today = date.today()
    with Session() as session:
        # Pobranie pojazdów oznaczonych jako niedostępne
        unavailable_vehs = session.query(Vehicle).filter(
            Vehicle.is_available == False
        ).all()

        # Zmiana wyniku na listę ID
        unavailable_veh_ids = [veh.id for veh in unavailable_vehs]

        if not unavailable_veh_ids:
            return []

        # Sprawdzanie, które sa wypożyczone dzisiaj
        rented_today = session.query(RentalHistory).filter(
            and_(
                RentalHistory.vehicle_id.in_(unavailable_veh_ids),
                RentalHistory.start_date <= today,
                today <= RentalHistory.end_date
            )
        ).all()

        # Sprawdzanie, które z nich są w naprawie dzisiaj
        repaired_today = session.query(RepairHistory).filter(
            and_(RepairHistory.vehicle_id.in_(unavailable_veh_ids),
                RepairHistory.start_date <= today,
                today <= RepairHistory.end_date
                )
        ).all()

        # Łączenie i zwracanie wyniku
        rented_ids = [vid[0] for vid in rented_today]
        repaired_ids = [vid[0] for vid in repaired_today]

        return list(set(rented_ids + repaired_ids))