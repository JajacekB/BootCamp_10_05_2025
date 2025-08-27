import sys
from PySide6.QtWidgets import QApplication
from requests import session

from database.base import SessionLocal
from gui.widgets.get_vehicle_view import GetVehicleView
from repositories.get_vehicle_service import GetVehicleService
from controllers.get_vehicle_controller import GetVehicleController


def main():
    session = SessionLocal()
    app = QApplication(sys.argv)
    view = GetVehicleView()
    service = GetVehicleService(session, view)
    controller = GetVehicleController(session, view)
    view.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()