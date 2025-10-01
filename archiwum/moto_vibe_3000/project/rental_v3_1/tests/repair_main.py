# repair_main.py
import sys
from PySide6.QtWidgets import QApplication
from database import SessionLocal  # Twój sessionmaker z SQLAlchemy
from gui.widgets.repair_view import RepairVehicleView
from controllers.repair_controller import RepairController

def main():
    app = QApplication(sys.argv)
    session = SessionLocal()
    view = RepairVehicleView()
    controller = RepairController(session, view)
    view.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()