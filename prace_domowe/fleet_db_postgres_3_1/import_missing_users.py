import sqlite3
from datetime import datetime
from fleet_database import SessionLocal
from fleet_models_db import User


def import_missing_users(sqlite_path):
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_conn.row_factory = sqlite3.Row
    cursor = sqlite_conn.cursor()

    session = SessionLocal()
    added = 0
    skipped = 0

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    for row in users:
        # Sprawdź czy user istnieje po loginie (unikalne pole)
        exists = session.query(User).filter_by(login=row['login']).first()
        if exists:
            skipped += 1
            continue

        user = User(
            id=row['id'],  # zachowaj oryginalne ID
            role=row['role'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            login=row['login'],
            phone=row['phone'],
            email=row['email'],
            password_hash=row['password_hash'],
            address=row['address'],
            registration_day=datetime.strptime(row['registration_day'], "%Y-%m-%d").date() if row[
                'registration_day'] else None
        )
        session.add(user)
        added += 1

    session.commit()
    session.close()
    sqlite_conn.close()

    print(f"Dodano użytkowników: {added}")
    print(f"Pominięto użytkowników (już istnieli): {skipped}")


if __name__ == "__main__":
    import_missing_users("fleet.db")