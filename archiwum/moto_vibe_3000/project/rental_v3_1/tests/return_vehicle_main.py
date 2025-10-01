import sys
import random
from PySide6.QtWidgets import QApplication

from database import SessionLocal
from gui.widgets.return_vehicle_view import ReturnVehicleView
from repositories.return_vehicle_service import ReturnVehicleService
from controllers.return_vehicle_controller import ReturnVehicleController
from models.user import User


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
    view = ReturnVehicleView(role="client")
    service = ReturnVehicleService(session, user)
    controller = ReturnVehicleController(session, view, service, user)
    view.set_controller(controller)
    view.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()