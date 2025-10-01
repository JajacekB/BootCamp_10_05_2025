import sys
from PySide6.QtWidgets import QApplication

from database import SessionLocal
from gui import DeleteVehicleView

from controllers.delete_vehicle_controller import DeleteVehicleController


def main():
    session = SessionLocal()
    app = QApplication()
    view = DeleteVehicleView()
    controller = DeleteVehicleController(session, view)
    view.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()

