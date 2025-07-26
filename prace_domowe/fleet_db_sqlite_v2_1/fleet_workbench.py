from fleet_models_db import Vehicle, Car, Scooter, Bike, User, RentalHistory, RepairHistory, Invoice, Promotion
from sqlalchemy import func, cast, Integer, extract, and_, or_, exists, select, desc, asc
from sqlalchemy.exc import IntegrityError
from fleet_database import Session, SessionLocal
from datetime import date, datetime, timedelta
from collections import defaultdict
from fleet_manager_user import get_clients, get_users_by_role
from fleet_utils_db import (
    get_positive_int, calculate_rental_cost, recalculate_cost, get_positive_float, get_return_date_from_user,
    generate_vehicle_id, get_available_vehicles, get_unavailable_vehicle, generate_repair_id)
import bcrypt


def repair_vehicle(user):
    print(f"\n{ '>>> NAPRAW POJAZDÓW <<<':^30 }")
    with SessionLocal() as session:
        # available_vehicles = get_available_vehicles(session)
        # if not available_vehicles:
        #     print("Brak dostępnych pojazdów do naprawy.")
        #     return
        #
        # print("\nDostępne pojazdy do naprawy:")
        # for v in available_vehicles:
        #     print(f"- {v.vehicle_model} ({v.type}), ID: {v.id}, Numer: {v.individual_id}")

        try:
            vehicle_id = int(input("Podaj ID pojazdu do przekazania do naprawy: "))
        except ValueError:
            print("Błędne ID.")
            return

        vehicle = session.query(Vehicle).filter_by(id=vehicle_id, is_available=True).first()
        if not vehicle:
            print("Nie znaleziono pojazdu.")
            return

        workshops = get_users_by_role("workshop", session)
        if not workshops:
            print("Brak zdefiniowanych użytkowników warsztatu.")
            return

        print("\nDostępne warsztaty:")
        for idx, w in enumerate(workshops, 1):
            print(f"{idx}. {w.first_name} {w.last_name} ({w.login})")

        # sprawdzanie czy pjazd jest wynajęty
        # rekalkulacj kosztów klienta
        # akceptacja przez klienta

        workshop_choice = get_positive_int("Wybierz numer warsztatu: ") - 1
        selected_workshop = workshops[workshop_choice]

        repair_days = get_positive_int("Podaj liczbę dni naprawy: ")
        planned_end_date = datetime.today().date() + timedelta(days=repair_days)

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
                planned_end_date=planned_end_date,
                actual_return_date=None,  # Domyślnie brak
                cost=repair_cost,
                description=description
            )
            session.add(repair)

            # Aktualizacja pojazdu
            vehicle.is_available = False
            vehicle.borrower_id = selected_workshop.id
            vehicle.return_date = planned_end_date  # Jeśli jeszcze używasz tej kolumny w Vehicle

            session.commit()
            print(
                f"\nPojazd {vehicle.brand} {vehicle.vehicle_model} {vehicle.individual_id}"
                f"\nprzekazany do warsztatu: {selected_workshop.first_name} {selected_workshop.last_name} do dnia {planned_end_date}."
            )
            return


def new_client_cost():

    # do usunięcia po wklejeniu wyżej
    with Session() as session:
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
    # dotąd usunąć

        broken_veh_id = get_positive_int("\nPodaj id pojadu do naprawy: ")

        broken_veh = session.query(Vehicle).filter(Vehicle.id == broken_veh_id).first()
        if broken_veh.is_available == False:
            broken_rent = session.query(RentalHistory).filter(RentalHistory.vehicle_id == broken_veh_id).first()

            today = date.today()
            broken_rental_id = broken_rent.id
            broken_rental_reservation_id = broken_rent.reservation_id
            broken_start_date = broken_rent.start_date
            broken_end_date = broken_rent.planned_return_date
            broken_veh_user_id = broken_rent.user_id
            broken_veh_cost_per_day = broken_veh.cash_per_day

            broken_veh_user = session.query(User).filter(User.id == broken_veh_user_id).first()

            if today < broken_end_date:

                approve_new_cost = input(
                    "\nCzy klient chce kontynuować najem?"
                    "\nWybierz (tak/nie): "
                ).strip().lower()

                while True:
                    if approve_new_cost in ("nie", "n", "no"):
                        new_client_cost = recalculate_cost(session, broken_veh_user, broken_end_date, broken_rental_reservation_id)

                    elif approve_new_cost in ("tak", "t", "yes", "y"):
                        nev_veh_for_client = session.query(Vehicle).filter(
                            Vehicle.cash_per_day == broken_veh_cost_per_day,
                            Vehicle.is_available == True,
                        ).first()

                        # Update popsuty pojazd, nowy pojazd


                        if not nev_veh_for_client:
                            """
                            """






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