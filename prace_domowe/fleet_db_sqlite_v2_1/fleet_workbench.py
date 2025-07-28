from fleet_models_db import Vehicle, Car, Scooter, Bike, User, RentalHistory, RepairHistory, Invoice, Promotion
from fleet_choices_menus import choice_menu, yes_or_not_menu
from sqlalchemy import func, cast, Integer, extract, and_, or_, exists, select, desc, asc
from sqlalchemy.exc import IntegrityError
from fleet_database import Session, SessionLocal
from datetime import date, datetime, timedelta
from collections import defaultdict
from fleet_manager_user import get_clients, get_users_by_role
from fleet_utils_db import (
    get_positive_int, calculate_rental_cost, recalculate_cost, get_positive_float, get_return_date_from_user,
    generate_vehicle_id, get_available_vehicles, get_unavailable_vehicle, generate_repair_id, update_database,
)
import bcrypt




def repair_vehicle_production():
    with Session() as session:

        # pobranie i wyświetlenie wszytskich pojazdów z podziałem na wynajęte i wolne
        rented_broken_vehs, _ = get_unavailable_vehicle(session)
        available_broken_vehs = get_available_vehicles(session)

        if not rented_broken_vehs:
            print("\n\n🚫 Brak niedostępnych pojazdów na dziś.")

        else:
            table_wide = 58
            print(
                f"\nPojazdy wynajęte:"
                f"\n|{'ID':>5}| {'Marka':<13}| {'Model':<13}| {'Nr w kartotece':<19}|"
            )
            print(table_wide * '-')
            for index, vehicle in enumerate(rented_broken_vehs, start=1):
                print(
                    f"| {vehicle.id:>4}| {vehicle.brand:<13}| {vehicle.vehicle_model:13}| {vehicle.individual_id:<19}|"
                )
        if not available_broken_vehs:
            print("\n🚫 Brak dostępnych pojazdów na dziś.")

        else:
            table_wide = 58
            print(
                f"\nPojazdy bez wynajmu:"
                f"\n|{'ID':>5}| {'Marka':<13}| {'Model':<13}| {'Nr w kartotece':<19}|"
            )
            print(table_wide * '-')
            for index, vehicle in enumerate(available_broken_vehs, start=1):
                print(
                    f"| {vehicle.id:>4}| {vehicle.brand:<13}| {vehicle.vehicle_model:13}| {vehicle.individual_id:<19}|"
                )

        # wybór niesprawnego pojazdu
        broken_veh_id = get_positive_int("\nPodaj id pojadu do naprawy: ")
        repair_days = get_positive_int(f"Podaj szacunkową ilość dni naprawy: ")

        today = date.today()
        planned_end_date = datetime.today().date() + timedelta(days=repair_days)

        broken_veh = session.query(Vehicle).filter(
            Vehicle.id == broken_veh_id
        ).first()

        # sprawdzenie czy pojazd ma aktywny najem
        broken_rent = session.query(RentalHistory).filter(
            RentalHistory.vehicle_id == broken_veh_id,
            today <= RentalHistory.planned_return_date,
            RentalHistory.start_date <= planned_end_date
        ).first()

        # jeśli brak najmu - oddanie do naprawy
        if not broken_rent:
            # mark_as_under_repair(session, broken_veh, repair_days)
            return True

        # jeśli pojazd został uszkodzony podczas najmu uruchomienie procedury wymiany pojazdu i rekalkulacji kosztów
        process_vehicle_swap_and_recalculate(session, broken_veh, broken_rent, repair_days)






        exit()


def process_vehicle_swap_and_recalculate(session, broken_veh, broken_rental, repair_days):
    choice = yes_or_not_menu(
        "Czy klient będzie kontynuował wynajem?"
    )
    if not choice:
        #klient kończy najem
        print("\nKlient kończy najem pojazdu.")

        broken_rental_total_cost, broken_rental_late_fee, _  = recalculate_cost(
            session, broken_veh.borrower, broken_veh, date.today(), broken_rental.reservation_id
        )

        print(
            f"\n💸 — KKW (Rzeczywisty Koszt Wynajmu) wynosi: {broken_rental_total_cost} zł"
            f" w tym {broken_rental_late_fee} zł za opóźnienie.")

        update_database(
            session, broken_veh, date.today(), broken_rental_total_cost,
            broken_rental_late_fee, broken_rental.reservation_id,
        )
        mark_as_under_repair(session, broken_veh, repair_days)
        return True

    #klient kontynuuje najem
    print("\nKlient kontynuuje najem pojazdu.")
    start_date = date.today()
    planned_return_date = broken_rental.planned_return_date

    # wyszukanie pojazdu zastępczego
    replacement_vehicle_list = get_available_vehicles(session, start_date, planned_return_date, broken_veh.type)

    replacement_vehicle = next(
        (v for v in replacement_vehicle_list if v.cash_per_day == broken_veh.cash_per_day),
        None
    )
    # jeśli znależiono pojazd zastępczy
    if replacement_vehicle:

        print(
            f"\nWydano klientowi pojazd zastępczy: {replacement_vehicle} \n"
            f"Oddano do naprawy: {broken_veh}"
        )
        update_database_after_vehicle_swap(
            session, broken_veh, replacement_vehicle, broken_rental, repair_days)
        mark_as_under_repair(
            session, broken_veh, repair_days)
        return True

    # gdy nie ma pojazdu w cenie niesprawnego pojazdu
    question = {
        "(D)": "Klient wybrał droższy pojazd jako zastępczy.",
        "(T)": "Klient wybral tańszy pojazd jako zastępczy.",
        "(A)": "Klient jednak anuluje wynajem."
    }

    decision = choice_menu(
        "Brak pojazdu w tej samej cenie. Czy klient decyduje sie na zmianę na droższy lub tańszy?", question
    )
    if decision is "a":
        # klient kończy najem
        print("\nKlient kończy najem pojazdu.")

        broken_rental_total_cost, broken_rental_late_fee, _ = recalculate_cost(
            session, broken_veh.borrower, broken_veh, date.today(), broken_rental.reservation_id
        )

        print(
            f"\n💸 — KKW (Rzeczywisty Koszt Wynajmu) wynosi: {broken_rental_total_cost} zł"
            f" w tym {broken_rental_late_fee} zł za opóźnienie.")

        update_database(
            session, broken_veh, date.today(), broken_rental_total_cost,
            broken_rental_late_fee, broken_rental.reservation_id,
        )
        mark_as_under_repair(session, broken_veh, repair_days)
        return True

    elif decision is "t":
        # wyszukanie tańczego pojazdu:
        lower_price_vehicle = find_replacement_vehicle(
            session, broken_veh, planned_return_date, True
        )

        if not lower_price_vehicle:

            choice = yes_or_not_menu(
                "Czy klient będzie zgadza się na wynajem droższego pojazdu?"
            )

            if not choice:

                lower_price_vehicle = find_replacement_vehicle(
                    session, broken_veh, planned_return_date, True
                )




    else:



        exit()


def find_replacement_vehicle(session, reference_vehicle, planned_return_date, prefer_cheaper: bool):
    # szukanie pojazdu z flagą preffer_cheeper
    available_vehicles = get_available_vehicles(
        session, date.today(), planned_return_date, reference_vehicle.type
    )

    if prefer_cheaper:
        # Najdroższy z tańszych
        vehicle = next(
            (v for v in sorted(available_vehicles, key=lambda v: v.cash_per_day, reverse=True)
            if v.cash_per_day < reference_vehicle.cash_per_day),
            None
        )
    else:
        # Najtańszy z droższych
        vehicle = next(
            (v for v in sorted(available_vehicles, key=lambda v: v.cash_per_day)
            if v.cash_per_day > reference_vehicle.cash_per_day),
            None
        )

    return vehicle





def update_database_after_vehicle_swap(
        session, original_vehicle, replacement_vehicle, broken_rental, repair_days):

    # rozdzielenie kosztów najmu na pojazdy zepsuty i zastępczy
    old_rental_cost = broken_rental.base_cost
    old_rental_period = (broken_rental.planned_return_date - broken_rental.start_date).days
    old_real_rental_period = (date.today() - broken_rental.planned_return_date).days

    broken_veh_cost = old_rental_cost * old_real_rental_period / old_rental_period
    replacement_veh_cost = old_rental_cost - broken_veh_cost

    # aktualizacja statusu pojazdu zwracanego
    original_vehicle.is_awaialable = True
    original_vehicle.borrower_id = None
    original_vehicle.return_date = None

    # aktualizacja statusu pojazdu wynajmowanego
    replacement_vehicle.is_available = None
    replacement_vehicle.borrower_id = broken_rental.user_id
    replacement_vehicle.return_date = broken_rental.planned_return_date

    # generowanie najmu pojazdu zastępczego
    replacement_rental = RentalHistory(
        reservation_id=broken_rental.reservation_id,
        user_id=broken_rental.user_id,
        vehicle_id=replacement_vehicle.vehicle_id,
        start_date=date.today(),
        planned_return_date=broken_rental.planned_return_date,
        base_cost=replacement_veh_cost,
        total_cost=replacement_veh_cost
    )
    session.add(replacement_rental)
    session.commit()











def mark_as_under_repair(session, vehicle, repair_days):
    workshops = get_users_by_role(session,"workshop",)
    if not workshops:
        print("Brak zdefiniowanych użytkowników warsztatu.")
        return

    print("\nDostępne warsztaty:")
    for idx, w in enumerate(workshops, 1):
        print(f"{idx}. {w.first_name} {w.last_name} ({w.login})")

    workshop_choice = get_positive_int("Wybierz numer warsztatu: ", max_value=len(workshops)) - 1
    selected_workshop = workshops[workshop_choice]

    planned_end_date = date.today() + timedelta(days=repair_days)

    repair_cost_per_day = get_positive_float("\nPodaj jednostkowy koszt naprawy: ")
    repair_cost = repair_cost_per_day * repair_days

    description = input("\nKrótko opisz zakres naprawy: ")

    repair_id = generate_repair_id()

    # Generowanie naprawy
    repair = RepairHistory(
        repair_id=repair_id,
        vehicle_id=vehicle.id,
        mechanic_id=selected_workshop.id,
        start_date=date.today(),
        planned_end_date=planned_end_date,
        actual_return_date=None,
        cost=repair_cost,
        description=description
    )
    session.add(repair)

    # Aktualizacja pojazdu
    vehicle.is_available = False
    vehicle.borrower_id = selected_workshop.id
    vehicle.return_date = planned_end_date

    session.commit()
    print(
        f"\nPojazd {vehicle.brand} {vehicle.vehicle_model} {vehicle.individual_id}"
        f"\nprzekazany do warsztatu: {selected_workshop.first_name} {selected_workshop.last_name} do dnia {planned_end_date}."
    )
    return







new_client_cost()



# repair_vehicle()









# def start_test():
#     while True:
#         print("\n=== LOGOWANIE DO SYSTEMU ===")
#         login_or_email = input("\nLogin: ").strip()
#         password = input("Hasło: ").strip()
#
#         with Session() as session:
#             user = session.query(User).filter(
#                 (User.login == login_or_email) | (User.email == login_or_email)
#             ).first()
#
#             if not user:
#                 print("\nNie znaleziono użytkownika.")
#             elif not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
#                 print("\nBłędne hasło.")
#             else:
#                 print(f"\nZalogowano jako {user.first_name} {user.last_name} ({user.role})")
#             role_test(user, session)
#             return user
#
# def role_test(user: User, session=None):
#     if session is None:
#         with Session() as session:
#             return role_test(user, session=session)
#
#     if user.role == "client":
#         vehicles = session.query(Vehicle).filter(Vehicle.borrower_id == user.id).order_by(Vehicle.return_date.asc()).all()
#
#         print(type(vehicles))
#
#
#     else:
#         print("Lipa")
#         unavailable_veh = session.query(Vehicle).filter(Vehicle.is_available != True).all()
#         unavailable_veh_ids = [v.id for v in unavailable_veh]
#
#         if not unavailable_veh:
#             print("\nBrak wynajętych pojazdów")
#             return
#
#         # lista wynajętych pojazdów
#         rented_vehs = session.query(RentalHistory).filter(
#             RentalHistory.vehicle_id.in_(unavailable_veh_ids)
#         ).order_by(RentalHistory.planned_return_date.asc()).all()
#
#         rented_ids = [r.vehicle_id for r in rented_vehs]
#
#         vehicles = session.query(Vehicle).filter(Vehicle.id.in_(rented_ids)).order_by(Vehicle.return_date).all()
#
#
#     table_wide = 91
#     month_pl = {
#         1: "styczeń",
#         2: "luty",
#         3: "marzec",
#         4: "kwiecień",
#         5: "maj",
#         6: "czerwiec",
#         7: "lipiec",
#         8: "sierpień",
#         9: "wrzesień",
#         10: "październik",
#         11: "listopad",
#         12: "grudzień"
#     }
#
#     veh_ids = [z.id for z in vehicles]
#
#     print(f"\nLista wynajętych pojazdów:\n")
#     print(
#         f"|{'ID.':>5}|{'Data zwrotu':>21} | {'Marka':^14} | {'Model':^14} |{'Nr rejestracyjny/seryjny':>25} |"
#     )
#     print(table_wide * "_")
#     for p in vehicles:
#         date_obj = p.return_date
#         day = date_obj.day
#         month_name = month_pl[date_obj.month]
#         year = date_obj.year
#         date_str = f"{day}-{month_name}_{year}"
#
#         print(
#             f"|{p.id:>4} |{date_str:>21} |{p.brand:>15} |{p.vehicle_model:>15} | {p.individual_id:>24} |"
#         )


# def return_vehicle():
#     # user = get_users_by_role()
#     # Pobieranie aktywnie wynajętych i zarejestrowanych pojazdów
#     with Session() as session:
#
#         unavailable_veh = session.query(Vehicle).filter(Vehicle.is_available != True).all()
#         unavailable_veh_ids = [v.id for v in unavailable_veh]
#
#         if not unavailable_veh:
#             print("\nBrak wynajętych pojazdów")
#             return
#
#         # lista wynajętych pojazdów
#         rented_vehs = session.query(RentalHistory).filter(
#             RentalHistory.vehicle_id.in_(unavailable_veh_ids)
#         ).order_by(RentalHistory.planned_return_date.asc()).all()
#
#         rented_ids = [r.vehicle_id for r in rented_vehs]
#
#         vehicles = session.query(Vehicle).filter(Vehicle.id.in_(rented_ids)).order_by(Vehicle.return_date).all()
#
#         table_wide = 91
#         month_pl = {
#             1: "styczeń",
#             2: "luty",
#             3: "marzec",
#             4: "kwiecień",
#             5: "maj",
#             6: "czerwiec",
#             7: "lipiec",
#             8: "sierpień",
#             9: "wrzesień",
#             10: "październik",
#             11: "listopad",
#             12: "grudzień"
#         }
#
#         veh_ids =[z.id for z in vehicles]
#         print(f"\n[DEBUG] baza vehicles: {veh_ids}")
#         print(f"\n[DEBUG] rented_ids: {rented_ids}")
#
#         print(f"\nLista wynajętych pojazdów:\n")
#         print(
#             f"|{'ID.':>5}|{'Data zwrotu':>21} | {'Marka':^14} | {'Model':^14} |{'Nr rejestracyjny/seryjny':>25} |"
#         )
#         print(table_wide * "_")
#         for p in vehicles:
#             date_obj = p.return_date
#             day = date_obj.day
#             month_name = month_pl[date_obj.month]
#             year = date_obj.year
#             date_str = f"{day}-{month_name}_{year}"
#
#             print(
#                 f"|{p.id:>4} |{date_str:>21} |{p.brand:>15} |{p.vehicle_model:>15} | {p.individual_id:>24} |"
#             ) # po wyczyszczeniu tabeli vehicles z braku dat zmienić na vehicle
#
#
#         # Wybór pojazdu do zwrotu i potwierdzenie chęci anulowania wynajmu lub rezerwacji
#         choice = get_positive_int(
#             f"\nKtóry pojazd chcesz zwrócić?"
#             f"\nPodaj nr ID: "
#         )
#
#         vehicle = session.query(Vehicle).filter(Vehicle.id == choice).first()
#         print(
#             f"\nCzy na pewno chcesz zwrócić pojazd: "
#             f"\n{vehicle}"
#         )
#         choice = input(
#             f"Wybierz (tak/nie): "
#         ).strip().lower()
#
#         if choice in ("nie", "n", "no"):
#             print("\nZwrot pojazdu anulowany.")
#             return
#
#         elif choice in ("tak", "t", "yes", "y"):
#             actual_return_date_input = get_return_date_from_user(session)
#             new_cost = recalculate_cost(session, vehicle, actual_return_date_input)

# def get_return_date_from_user(session) -> date:
#     while True:
#         return_date_input_str = input(
#             f"Podaj rzeczywistą datę zwrotu (DD-MM-YYYY) Enter = dziś: "
#         ).strip().lower()
#
#         try:
#
#             if return_date_input_str:
#                 return_date_input = datetime.strptime(return_date_input_str, "%d-%m-%Y").date()
#             else:
#                 return_date_input = date.today()
#             break
#
#         except ValueError:
#             print("❌ Niepoprawny format daty.")
#             continue
#     return return_date_input

# def recalculate_cost(session, vehicle: Vehicle, return_date: date):
#     # Rozdzielenie przypadków; przed czasem, aktualny, przeterminowany
#
#     planned_return_date = session.query(RentalHistory.planned_return_date).filter(
#         RentalHistory.vehicle_id == vehicle.id
#     ).order_by(RentalHistory.planned_return_date.desc()).scalar()
#
#     start_date = session.query(RentalHistory.start_date).filter(
#         RentalHistory.vehicle_id == vehicle.id
#     ).order_by(RentalHistory.planned_return_date.desc()).scalar()
#
#     base_cost = session.query(RentalHistory.base_cost).filter(RentalHistory.vehicle_id == vehicle.id).scalar()
#     cash_per_day = session.query(Vehicle.cash_per_day).filter(Vehicle.id == vehicle.id).scalar()
#
#     # user = session.query(RentalHistory.user_id).filter(RentalHistory.vehicle_id == vehicle.id).first()
#
#     if return_date > planned_return_date:
#         extra_days = (return_date - planned_return_date).days
#         total_cost = base_cost + extra_days * cash_per_day
#         overdue_fee_text = f"\n{base_cost} zł opłata bazowa + {extra_days * cash_per_day} zł kara za przeterminowanie.)"
#     elif return_date == planned_return_date:
#         total_cost = base_cost
#         overdue_fee_text = " (zwrot terminowy)"
#     else:
#         new_period = (planned_return_date - start_date).days
#         total_cost = calculate_rental_cost(user, cash_per_day, new_period)
#         overdue_fee_text = " (zwrot przed terminem, naliczono koszt zgodnie z czasem użytkowania)"
#
#     print(
#         f"\n💸 — KKW (Rzeczywisty Koszt Wynajmu) wynosi: {total_cost} zł.{overdue_fee_text}"
#     )
#     print(
#         f"\nCzy na pewno chcesz zwrócić pojazd: "
#         f"\n{vehicle}"
#     )
#     choice = input(
#         f"Wybierz (tak/nie): "
#     ).strip().lower()
#
#     if choice in ("nie", "n", "no"):
#         print("\nZwrot pojazdu anulowany.")
#         return
#
#     elif choice in ("tak", "t", "yes", "y"):
#         update_database(session, vehicle, return_date, total_cost)

# def update_database(session, vehicle: Vehicle, return_date: date, total_cost: float):
#
#     vehicle.is_available = True
#     vehicle.borrower_id = None
#     vehicle.return_date = None
#
#     rental = RentalHistory(
#         actual_return_date=return_date,
#         total_cost=total_cost
#     )
#
#     invoice = Invoice(
#         amount=total_cost
#     )
#
#     session.add_all([vehicle, rental, invoice])
#     session.commit()
#     return





# with Session() as session:
#     today = date.today()
#     unavailable_vehs = session.query(Vehicle).filter(Vehicle.is_available == False).all()
#     for v in unavailable_vehs:
#         # print(v)
#         print(v.id)
#
#     unavailable_veh_ids = [veh.id for veh in unavailable_vehs]
#     for veh_id in unavailable_veh_ids:
#         print(veh_id)
#         print(type(veh_id))
#
#     rentals = session.query(RentalHistory).filter(
#         and_(
#             RentalHistory.vehicle_id.in_(unavailable_veh_ids),
#             RentalHistory.start_date <= today,
#             today <= RentalHistory.end_date)
#     ).all()
#
#     for rental in rentals:
#         print(rental.vehicle_id)
#
#     print(111 * "2")
#
#     repaireds = session.query(RepairHistory).filter(
#         and_(RepairHistory.vehicle_id.in_(unavailable_veh_ids),
#             RepairHistory.start_date <= today,
#             today <= RepairHistory.end_date)
#     ).all()
#
#     for repaired in repaireds:
#         print(repaired.vehicle_id)
#
#     print(111 * '#')
#
#     unavailable_vehs = rentals + repaireds
#
#     for unaval in unavailable_vehs:
#         print(unaval.vehicle_id)





# #def rent_vehicle():
# print("\n>>> Przeglądanie pojazdów <<<")
# start_date_input_str = input(f"\nPodaj datę początku wynajmu w formacie YYYY-MM-DD: ").strip()
# end_time_input_str = input(f"Podaj datę końca wynajmu w formacie YYYY-MM-DD: ").strip()
# start_date_input = datetime.strptime(start_date_input_str, "%Y-%m-%d").date()
# end_time_input = datetime.strptime(end_time_input_str, "%Y-%m-%d").date()
#
# delta_input = end_time_input - start_date_input
#
# print(f"\nIlość dni: {delta_input.days}")
# print(type(delta_input))
#
# with Session() as session:
#     conflikt_condition_input = and_(
#         RentalHistory.start_date <= end_time_input,
#         RentalHistory.end_date >= start_date_input
#     )
#     conflicted_vehicle = session.query(RentalHistory.vehicle_id).filter(conflikt_condition_input).conflicted_vehicle()
#
#     available_vehicle = session.query(Vehicle).filter(
#         ~Vehicle.id.in_(conflicted_vehicle)
#     ).all()
#
#
#
#
#
#


# users = session.query(User).filter(User.role != "admin").all()
# for user in users:
#     print(user)
#
#
# def delete_user():
#     login_to_delete = input("Podaj login użytkownika do usunięcia: ").strip()
#     user = session.query(User).filter_by(login=login_to_delete).first()
#
#     if not user:
#         print("Nie znaleziono użytkownika.")
#         return
#
#     if user.role == "admin":
#         print("Nie można usunąć konta administratora systemowego.")
#         return
#
#     session.delete(user)
#     session.commit()
#     print(f"Użytkownik {login_to_delete} został usunięty.")


# from sqlalchemy.orm import Session
#
# with Session(engine) as session:
#     new_id = generate_vehicle_id(session, "CAR")
#     print(new_id)  # np. CAR001, CAR002 itd.
#
#     new_car = Car(vehicle_id=new_id, brand="Toyota", vehicle_model="Corolla",
#                   cash_per_day=150.0, size="M", fuel_type="petrol")
#
#     session.add(new_car)
#     session.commit()