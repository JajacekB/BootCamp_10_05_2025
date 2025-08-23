# repositories/write_methods.py
from models.user import User
from database.base import SessionLocal
from sqlalchemy.exc import IntegrityError


def update_user(session, user: User, data: dict):
    """
    Aktualizuje dane użytkownika i commit do bazy.
    data: {"first_name": ..., "last_name": ..., "email": ..., "phone": ..., "address": ...}
    """
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