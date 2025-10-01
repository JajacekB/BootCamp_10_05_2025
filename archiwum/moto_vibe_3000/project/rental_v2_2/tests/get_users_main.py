# main_consol_version.py
from PySide6.QtWidgets import QApplication
from database import SessionLocal
from gui import GetUsersWidget
from repositories.get_users_service import GetUsersService
from controllers.get_users_controller import GetUsersController

def main():
    app = QApplication([])

    session = SessionLocal()
    service = GetUsersService(session)
    view = GetUsersWidget()
    controller = GetUsersController(view, service)

    view.show()
    app.exec()

if __name__ == "__main__":
    main()