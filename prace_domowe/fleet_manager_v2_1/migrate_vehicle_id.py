from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fleet_models_db import Vehicle, RentalHistory  # Załaduj swoje modele
from fleet_database import Base  # jeśli potrzebne

# Podstawowa konfiguracja bazy
engine = create_engine("sqlite:///fleet.db")  # zmień ścieżkę do swojej bazy
Session = sessionmaker(bind=engine)

def migrate_vehicle_id_in_rental_history():
    session = Session()

    try:
        # 1. Pobierz mapę vehicle_id_string -> id_int
        vehicles = session.query(Vehicle).all()
        mapping = {v.vehicle_id: v.id for v in vehicles}

        print(f"Znaleziono {len(mapping)} pojazdów do mapowania.")

        # 2. Pobierz wszystkie wpisy w rental_history
        rentals = session.query(RentalHistory).all()
        print(f"Przetwarzam {len(rentals)} wpisów w historii wypożyczeń...")

        count_updated = 0
        for rental in rentals:
            if rental.vehicle_id in mapping:
                old_value = rental.vehicle_id
                rental.vehicle_id = mapping[old_value]
                count_updated += 1
            else:
                print(f"⚠️ Nie znaleziono pojazdu o vehicle_id='{rental.vehicle_id}' w tabeli vehicles!")

        session.commit()
        print(f"✅ Zaktualizowano {count_updated} rekordów w rental_history.")

    except Exception as e:
        session.rollback()
        print(f"❌ Wystąpił błąd: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    migrate_vehicle_id_in_rental_history()