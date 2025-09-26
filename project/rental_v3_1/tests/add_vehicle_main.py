import sys
from PySide6.QtWidgets import QApplication

from database.base import SessionLocal
from gui.widgets.add_vehicle_view import AddVehicleView
from controllers.add_vehicle_controller import AddVehicleController


def main():

    session = SessionLocal()
    app = QApplication(sys.argv)
    view = AddVehicleView()
    controller = AddVehicleController(session, view ,"seller")

    view.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()




