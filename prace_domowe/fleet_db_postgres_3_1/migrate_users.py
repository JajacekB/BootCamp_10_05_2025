import sqlite3
from sqlalchemy.orm import sessionmaker
from fleet_database import engine
from fleet_models_db import User

Session = sessionmaker(bind=engine)

def migrate_users(sqlite_db_path='fleet.db'):
    # Połączenie do SQLite
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    cursor = sqlite_conn.cursor()

    # Pobieramy wszystkie rekordy z users
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    session = Session()

    # Dodajemy każdego usera do PostgreSQL
    for row in rows:
        data = dict(zip(columns, row))

        # Uwaga: jeśli w SQLite masz np. kolumnę 'password_hash' a w modelu jest 'password_hash'
        # to musi się zgadzać nazwa klucza. Jeśli nie, dostosuj tutaj.
        user = User(**data)
        session.add(user)

    session.commit()
    session.close()
    sqlite_conn.close()
    print(f"✅ Przeniesiono {len(rows)} użytkowników z SQLite do PostgreSQL.")


if __name__ == "__main__":
    migrate_users()



