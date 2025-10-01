# delete_users_controller.py
from PySide6.QtWidgets import QMessageBox

from gui import DeleteUsersWidget
from repositories.delete_users_service import DeleteUsersService

class DeleteUsersController:
    def __init__(self, view: DeleteUsersWidget, service: DeleteUsersService):
        self.view = view
        self.service = service

        self.view.request_users.connect(self.load_users)
        self.view.user_selected.connect(self.show_user_summary)
        self.view.delete_requested.connect(self.delete_user)
        self.view.cancel_requested.connect(self.reset_summary)

    def load_users(self):
        users = self.service.get_candidates()
        self.view.populate_users(users)

    def show_user_summary(self, uid: int):
        info = self.service.get_user_details(uid)
        if info:
            self.view.show_user_summary(info)

    def delete_user(self, uid: int):
        success = self.service.deactivate_user(uid)
        if success:
            QMessageBox.information(self.view, "Sukces", "Użytkownik został dezaktywowany.")
        self.view.reset_summary()

    def reset_summary(self):
        self.view.reset_summary()



