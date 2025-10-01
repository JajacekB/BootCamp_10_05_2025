import sys
from PySide6.QtWidgets import QApplication

from database import SessionLocal
from gui.widgets.overdue_rental_view import OverdueRentalView
from controllers.overdue_rental_controller import OverdueRentalController


def main():

    session = SessionLocal()
    app = QApplication(sys.argv)
    view = OverdueRentalView(role="seller")
    controller = OverdueRentalController(session, view, "seller")

    view.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
