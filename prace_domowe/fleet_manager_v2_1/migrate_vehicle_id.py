

from sqlalchemy import text
from datetime import date
from fleet_database import engine, Session
from fleet_manager_user import User

# --- Dodajemy kolumny do istniejących tabel ---
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE vehicles ADD COLUMN purchase_date DATE"))
        print("✅ Dodano kolumnę purchase_date do vehicles.")
    except Exception as e:
        print(f"(INFO) purchase_date już istnieje lub błąd: {e}")

    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN registration_day DATE"))
        print("✅ Dodano kolumnę registration_day do users.")
    except Exception as e:
        print(f"(INFO) registration_day już istnieje lub błąd: {e}")

# --- Opcjonalnie: ustawiamy datę rejestracji adminowi ---
with Session() as session:
    admin = session.query(User).filter_by(role='Admin').first()
    if admin:
        admin.registration_day = date.today()
        session.commit()
        print("✅ Zaktualizowano datę rejestracji admina.")
    else:
        print("⚠️ Nie znaleziono admina w bazie.")