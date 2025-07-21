from fleet_database import SessionLocal
from fleet_models_db import User

def test_add_user():
    with SessionLocal() as session:
        user = User(
            first_name="Jan",
            last_name="Kowalski",
            address="ul. Przykładowa 1",
            email="jan.kowalski@example.com",
            password_hash="hashed_dummy",  # <-- tu poprawka
            role="Client",
            login="jankowalski",
            phone="123456789"
        )
        session.add(user)
        session.commit()
        print("✅ Użytkownik dodany.")

if __name__ == "__main__":
    test_add_user()