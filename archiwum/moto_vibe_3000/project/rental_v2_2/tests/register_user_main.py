import sys
from PySide6.QtWidgets import QApplication

from database import SessionLocal
from controllers.register_user_controller import RegisterUserController
from gui import RegisterUserView


def main():
    app = QApplication(sys.argv)
    session = SessionLocal()
    view = RegisterUserView()
    controller = RegisterUserController(session, view)
    view.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()