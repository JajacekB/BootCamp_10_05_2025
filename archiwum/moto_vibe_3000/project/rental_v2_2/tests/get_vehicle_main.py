import sys
from PySide6.QtWidgets import QApplication

from database import SessionLocal
from gui import GetVehicleView
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