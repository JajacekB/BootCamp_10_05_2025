# main.py
from PySide6.QtWidgets import QApplication
from database.base import SessionLocal
from gui.widgets.get_users_view import GetUsersWidget
from logic.get_users_service import GetUsersService
from gui.controllers.get_users_controller import GetUsersController

def main():
    app = QApplication([])

    session = SessionLocal()          # sesja do bazy
    service = GetUsersService(session)   # serwis z logiką
    view = GetUsersWidget()              # widok nie przyjmuje sesji!
    controller = GetUsersController(view, service)

    view.show()
    app.exec()

if __name__ == "__main__":
    main()