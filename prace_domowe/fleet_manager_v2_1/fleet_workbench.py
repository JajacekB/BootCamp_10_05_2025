

users = session.query(User).filter(User.role != "admin").all()
for user in users:
    print(user)


def delete_user():
    login_to_delete = input("Podaj login użytkownika do usunięcia: ").strip()
    user = session.query(User).filter_by(login=login_to_delete).first()

    if not user:
        print("Nie znaleziono użytkownika.")
        return

    if user.role == "admin":
        print("Nie można usunąć konta administratora systemowego.")
        return

    session.delete(user)
    session.commit()
    print(f"Użytkownik {login_to_delete} został usunięty.")





from sqlalchemy.orm import Session

with Session(engine) as session:
    new_id = generate_vehicle_id(session, "CAR")
    print(new_id)  # np. CAR001, CAR002 itd.

    new_car = Car(vehicle_id=new_id, brand="Toyota", vehicle_model="Corolla",
                  cash_per_day=150.0, size="M", fuel_type="petrol")

    session.add(new_car)
    session.commit()