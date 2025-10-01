import sys
import random
from PySide6.QtWidgets import QApplication

from models.user import User
from database import SessionLocal
from gui import UpdateUserView
from controllers.update_user_controller import UpdateUserController

def main():

    session = SessionLocal()

    client_ids = [u.id for u in session.query(User).filter(User.role == "client").all()]
    if not client_ids:
        print("Brak klientów w bazie!")
        return

    random_id = random.choice(client_ids)
    user = session.get(User, random_id)

    print(f"✅ Wylosowano klienta: {user.first_name} {user.last_name} (id={user.id})")

    app = QApplication(sys.argv)
    view = UpdateUserView(user)
    controller = UpdateUserController(session, view, user)
    view.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
