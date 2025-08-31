# directory: services
# file: database_update.py
import re
from sqlalchemy import or_

from datetime import date
from models.vehicle import Vehicle
from models.rental_history import RentalHistory
from models.invoice import Invoice


def update_database(
        session,
        vehicle: Vehicle,
        return_date: date,
        total_cost: float,
        late_fee: float,
        reservation_id: str):
    try:
        if reservation_id[-1].isalpha():
            reservation_id_cut = reservation_id[:-1]
            rental_cut = session.query(RentalHistory).filter(
                RentalHistory.reservation_id == reservation_id_cut
            ).first()
            rental = session.query(RentalHistory).filter(
                RentalHistory.reservation_id == reservation_id
            ).first()

            rental_id = rental_cut.id

            invoice = (
                session.query(Invoice)
                .filter(
                    Invoice.rental_id == rental_id
                )
                .first()
            )
            if not invoice:
                print("Nie ma faktury o podanym numerze id.")
                return False

        else:
            rental = session.query(RentalHistory).filter(
                RentalHistory.reservation_id == reservation_id
            ).first()

            rental_id = rental.id

            invoice = (
                session.query(Invoice)
                .filter(
                Invoice.rental_id == rental_id
                )
                .first()
            )

            if not invoice:
                print("Nie ma faktury o podanym numerze id.")
                return False

        print(f"{reservation_id=} {return_date=}")

        vehicle.is_available = True
        vehicle.borrower_id = None
        vehicle.return_date = None

        rental.actual_return_date = return_date
        rental.total_cost=total_cost
        rental.late_fee = late_fee
        invoice.amount=total_cost

        session.add_all([vehicle, rental, invoice])
        session.commit()

        print("✅ Baza danych została pomyślnie zaktualizowana.")
        return True

    except Exception as e:
        session.rollback()
        print(f"❗ Wystąpił błąd podczas aktualizacji bazy danych: {e}")
        return False


