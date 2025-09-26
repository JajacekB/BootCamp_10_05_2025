# delete_users_main.py
import sys
from PySide6.QtWidgets import QApplication

from database.base import SessionLocal
from repositories.delete_users_service import DeleteUsersService
from gui.widgets.delete_users_view import DeleteUsersWidget
from controllers.delete_users_controller import DeleteUsersController


def main():

    app = QApplication(sys.argv)
    session = SessionLocal()
    view = DeleteUsersWidget(role="client")
    service = DeleteUsersService(session, role="client")
    controller = DeleteUsersController(view, service)
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()