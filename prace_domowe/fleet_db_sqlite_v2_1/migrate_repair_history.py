from datetime import date
from sqlalchemy.orm import Session
from fleet_database import SessionLocal
from fleet_models_db import RepairHistory

def fill_missing_actual_return_dates():
    with SessionLocal() as session:
        today = date.today()

        # Pobierz rekordy bez daty zakończenia
        repairs = session.query(RepairHistory).filter(
            RepairHistory.actual_return_date.is_(None),
            RepairHistory.planned_end_date <= today
        ).all()

        print(f"Znaleziono {len(repairs)} rekordów do aktualizacji.")

        for repair in repairs:
            repair.actual_return_date = repair.planned_end_date
            print(f"✔ Ustawiono actual_return_date dla naprawy {repair.repair_id} na {repair.planned_end_date}")

        session.commit()
        print("✅ Zmiany zapisane.")

if __name__ == "__main__":
    fill_missing_actual_return_dates()