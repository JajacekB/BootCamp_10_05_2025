from fleet_models_db import Vehicle, Car, Scooter, Bike, User, RentalHistory, Invoice, Promotion, RepairHistory
from fleet_database import Session, SessionLocal
from sqlalchemy import func, cast, Integer, extract, and_, or_, exists, select
from datetime import datetime, date, timedelta


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

def generate_invoice_number(planned_return_date):
    """
                Generuje numer faktury w formacie FV/YYYY/MM/NNNN
                - session: aktywna sesja SQLAlchemy
                - planned_return_date: data zakończenia wypożyczenia (datetime.date)
                """
    with Session() as session:

        year = planned_return_date.year
        month = planned_return_date.month

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

def generate_vehicle_id(prefix: str, session) -> str:
    prefix = prefix.upper()
    prefix_len = len(prefix)

    # Szukamy najwyższego numeru w bazie danych
    max_number_db = session.query(
        func.max(
            cast(func.substr(Vehicle.vehicle_id, prefix_len + 1), Integer)
        )
    ).filter(
        Vehicle.vehicle_id.ilike(f"{prefix}%")
    ).scalar() or 0

    # Szukamy najwyższego numeru w obiektach dodanych do sesji (tymczasowych)
    max_number_pending = 0
    for obj in session.new:
        if isinstance(obj, Vehicle) and obj.vehicle_id and obj.vehicle_id.startswith(prefix):
            try:
                number = int(obj.vehicle_id[prefix_len:])
                if number > max_number_pending:
                    max_number_pending = number
            except ValueError:
                continue

    # Bierzemy najwyższy z obu
    next_number = max(max_number_db, max_number_pending) + 1
    return f"{prefix}{next_number:03d}"

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

def get_unavailable_vehicle(session, start_date = None, planned_return_date = None, vehicle_type = "all"):
    today = date.today()
    if start_date is None or planned_return_date is None:
        start_date = planned_return_date = date.today()

    filters = [Vehicle.is_available == True]
    if vehicle_type != "all":
        filters.append(Vehicle.type == vehicle_type)

    rented_vehicles = session.query(RentalHistory).join(Vehicle).filter(
        *filters,
            RentalHistory.start_date <= planned_return_date,
            RentalHistory.planned_return_date >= start_date
        ).all()
    rented_ids = [r.vehicle_id for r in rented_vehicles]

    # 3. Pojazdy w naprawie dzisiaj
    repaired_today = session.query(RepairHistory).join(Vehicle).filter(
        *filters,
                RepairHistory.start_date <= planned_return_date,
                RepairHistory.planned_end_date >= start_date
        ).all()
    repaired_ids = [r.vehicle_id for r in repaired_today]

    unavailable_ids = list(set(rented_ids + repaired_ids))
    return unavailable_ids

def get_available_vehicles(session, start_date=None, planned_return_date=None, vehicle_type="all"):
    unavailable_ids = get_unavailable_vehicle(session, start_date, planned_return_date, vehicle_type)

    filters = [
        Vehicle.is_available == True,
        ~Vehicle.id.in_(unavailable_ids)  # przeciwieństwo
    ]
    if vehicle_type != "all":
        filters.append(Vehicle.type == vehicle_type)

    truly_available = session.query(Vehicle).filter(*filters).all()
    return truly_available

def show_vehicles_rented_today(session):
    today = date.today()

    # Wyszukaj wszystkie wypożyczenia trwające dziś
    rentals_today = session.query(RentalHistory).filter(
        and_(
            RentalHistory.start_date <= today,
            today <= RentalHistory.planned_return_date
        )
    ).all()

    if not rentals_today:
        print("\n✅ Dziś żaden pojazd nie jest wypożyczony.")
        return

    print("\n🚘 Pojazdy wypożyczone dziś:\n")

    for rental in rentals_today:
        vehicle = session.query(Vehicle).filter_by(id=rental.vehicle_id).first()
        user = session.query(User).filter_by(id=rental.user_id).first()

        print(
            f" [ID: {vehicle.id}]  {vehicle.brand} {vehicle.vehicle_model}"
            f"   ❌ Wypożyczony w terminie: {rental.start_date} → {rental.planned_return_date}"
            f"   👤 Klient ID {user.id}: {user.first_name} {user.last_name}\n"
        )
