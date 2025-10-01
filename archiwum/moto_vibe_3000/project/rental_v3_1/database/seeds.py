# directory: database
# file: seeds.py

import bcrypt
from database import SessionLocal
from models.user import User


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def add_workshop_users():
    session = SessionLocal()

    workshops = [
        {
            "login": "scooter",
            "password": "Scooter1",
            "first_name": "Mechanik",
            "last_name": "Szumni_Motor",
            "phone": "600555666",
            "email": "szumny.motors@gmail.com",
            "address": "ul. Krakowska 130, 32-088 Brzozówka"
        },
        {
            "login": "biker",
            "password": "Biker1",
            "first_name": "Serwis",
            "last_name": "Bike - Service",
            "phone": "600777888",
            "email": "service.bike@gmail.com",
            "address": "ul. Lwowska 23, 30-831 Kraków"
        }
    ]

    for w in workshops:
        existing_user = session.query(User).filter_by(login=w["login"]).first()
        if existing_user:
            print(f"Użytkownik {w['login']} już istnieje, pomijam.")
            continue

        hashed_password = hash_password(w["password"])

        user = User(
            role="workshop",
            first_name=w["first_name"],
            last_name=w["last_name"],
            login=w["login"],
            phone=w["phone"],
            email=w["email"],
            password_hash=hashed_password,
            address=w["address"]
        )
        session.add(user)

    session.commit()
    print("Dodano użytkowników warsztatu do bazy.")
    session.close()


if __name__ == "__main__":
    add_workshop_users()