from fleet_models_db import Vehicle, Car, Scooter, Bike
from sqlalchemy import func, cast, Integer, or_, and_, not_
from sqlalchemy.exc import IntegrityError
from fleet_database import Session
from datetime import date, datetime, timedelta
from fleet_models_db import RentalHistory, Invoice
from collections import defaultdict


#def rent_vehicle():
print("\n>>> Przeglądanie pojazdów <<<")
start_date_input_str = input(f"\nPodaj datę początku wynajmu w formacie YYYY-MM-DD: ").strip()
end_time_input_str = input(f"Podaj datę końca wynajmu w formacie YYYY-MM-DD: ").strip()
start_date_input = datetime.strptime(start_date_input_str, "%Y-%m-%d").date()
end_time_input = datetime.strptime(end_time_input_str, "%Y-%m-%d").date()

delta_input = end_time_input - start_date_input

print(f"\nIlość dni: {delta_input.days}")
print(type(delta_input))

with Session() as session:
    conflikt_condition_input = and_(
        RentalHistory.start_date <= end_time_input,
        RentalHistory.end_date >= start_date_input
    )
    conflicted_vehicle = session.query(RentalHistory.vehicle_id).filter(conflikt_condition_input).conflicted_vehicle()

    available_vehicle = session.query(Vehicle).filter(
        ~Vehicle.id.in_(conflicted_vehicle)
    ).all()








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