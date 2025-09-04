# directory: services
# file:  rental_cost.py

from datetime import date
from database.base import SessionLocal
from models.rental_history import RentalHistory
from models.promotions import Promotion
from models.user import User
from models.vehicle import Vehicle


def calculate_rental_cost(session, user, daily_rate, rental_days):
    session = session or SessionLocal

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
        if rental_days >= promo.min_days:
            discount = promo.discount_percent / 100.0
            print(f"\n✅ Przyznano rabat {int(promo.discount_percent)}% ({promo.description})")
            break

    # Cena po uwzględnieniu rabatu i 1 dnia gratis (jeśli przysługuje)
    paid_days = max(rental_days - loyalty_discount_days, 0)
    price = paid_days * daily_rate * (1 - discount)

    return round(price, 2), discount * 100, "lojalność + czasowy" if discount > 0 and loyalty_discount_days else (
        "lojalność" if loyalty_discount_days else (
        "czasowy" if discount > 0 else "brak rabatów"))


def recalculate_cost(session, user: User, vehicle: Vehicle, return_date: date, reservation_id: str):
    rental_looked = session.query(RentalHistory).filter(
        RentalHistory.reservation_id == reservation_id
    ).first()

    if not rental_looked:
        raise ValueError("Nie znaleziono rezerwacji o podanym ID")

    planned_return_date = rental_looked.planned_return_date
    start_date = rental_looked.start_date
    base_to_calculate = rental_looked.total_cost
    cash_per_day = vehicle.cash_per_day

    discount_info = ""

    if return_date < start_date:
        extra_fee = 0
        total_cost = cash_per_day
        case_text = f"📅 Rezerwacja anulowana przed rozpoczęciem. Opłata karna: {cash_per_day:.2f} zł."

    elif return_date > planned_return_date:
        extra_days = (return_date - planned_return_date).days
        extra_fee = extra_days * cash_per_day
        total_cost = base_to_calculate + extra_fee
        case_text = (
            f"⏰ Zwrot po terminie — opłata bazowa: {base_to_calculate:.2f} zł + "
            f"kara za {extra_days} dni spóźnienia: {extra_fee:.2f} zł."
        )

    elif return_date == planned_return_date:
        extra_fee = 0
        total_cost = base_to_calculate
        case_text = "✅ Zwrot terminowy — brak dodatkowych opłat."

    else:
        new_period = (return_date - start_date).days
        extra_fee = 0
        price, discount_percent, discount_type = calculate_rental_cost(session, user, cash_per_day, new_period)
        total_cost = price
        discount_info = (
            f" Rabat: {discount_percent:.0f}% ({discount_type})." if discount_type != "brak" else ""
        )
        case_text = (
            f"🏎 Zwrot przed terminem — opłata naliczona za {new_period} dni użytkowania: "
            f"{price:.2f} zł.{discount_info}"
        )


    summary_text = (
        f"\n💸 — KKW (Rzeczywisty Koszt Wynajmu): {total_cost:.2f} zł.\n"
        f"{case_text}"
    )

    return total_cost, extra_fee, summary_text


