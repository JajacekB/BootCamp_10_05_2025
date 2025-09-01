# repositories/write_methods.py
from models.user import User
from models.vehicle import Vehicle
from database.base import SessionLocal
from sqlalchemy.exc import IntegrityError


def update_user(session, user: User, data: dict):

    try:
        for key, value in data.items():
            setattr(user, key, value)
        session.commit()
        return True, "Zaktualizowano pomyślnie"

    except IntegrityError as e:
        session.rollback()
        return False, str(e)

    except Exception as e:
        session.rollback()
        return False, str(e)


def add_user(session, user: User):

    try:
        session.add(user)
        session.commit()
        session.refresh(user)

        role_dict = {
            "client": "kienta",
            "seller": "pracownika",
            "workshop": "warsztat",
            "admin": "adminstratora"
        }
        return True, f"Pomyślnie dodano nowego {role_dict.get(user.login, user.role)}"

    except IntegrityError as e:
        session.rollback()
        return False, "❌ Login, telefon lub email już istnieje."

    except Exception as e:
        session.rollback()
        return False, str(e)

def deactivate_vehicle(session, vehicle: Vehicle):

    if not vehicle:
        return False, f"Brak pojazdu o tych danych"

    try:
        vehicle.is_active = False
        session.commit()
        return True, (
            f"Pojazd [{vehicle.vehicle_id}] {vehicle.brand} "
            f"{vehicle.vehicle_model} o numerze {vehicle.individual_id} "
            f"został usunięty z eksploatacji.")
    except Exception as e:
        session.rollback()
        return False, (f"Nie udało się usunąc pojazd:"
                    f"[{vehicle.vehicle_id}] {vehicle.brand} "
                    f"{vehicle.vehicle_model} o numerze {vehicle.individual_id} "
                    f"z eksploatacji. szczegóły: {str(e)}")



