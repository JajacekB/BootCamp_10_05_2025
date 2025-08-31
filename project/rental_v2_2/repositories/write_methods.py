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
        return True, f"Pomyślnie dodano nowego {role_dict.get(user.role, user.role)}"

    except IntegrityError as e:
        session.rollback()
        return False, "❌ Login, telefon lub email już istnieje."

    except Exception as e:
        session.rollback()
        return False, str(e)

def update_vehicle(session, vehicle: Vehicle):
    try:
        """
        """
        # self.session.commit()
    except Exception as e:
        """
        """

