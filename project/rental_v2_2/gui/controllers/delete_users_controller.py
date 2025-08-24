# delete_users_controller.py
from PySide6.QtWidgets import QMessageBox

from gui.widgets.delete_users_view import DeleteUsersWidget
from logic.delete_users_service import DeleteUsersService

class DeleteUsersController:
    def __init__(self, view: DeleteUsersWidget, service: DeleteUsersService):
        self.view = view
        self.service = service

        # podłącz sygnały widoku do metod
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



# from PySide6.QtWidgets import QMessageBox
#
#
# class DeleteUsersController:
#     def __init__(self, view, service):
#         self.view = view
#         self.service = service
#
#         # połączenie sygnałów
#         self.view.request_users.connect(self.show_users)
#         self.view.user_selected.connect(self.show_user_summary)
#         self.view.delete_requested.connect(self.delete_user)
#         self.view.cancel_requested.connect(self.view.reset_summary)
#
#     def show_users(self):
#         try:
#             users = self.service.get_candidates()
#             self.view.populate_users(users)
#         except Exception as e:
#             QMessageBox.critical(self.view, "Błąd", f"Wystąpił problem podczas pobierania danych:\n{e}")
#
#     def show_user_summary(self, uid):
#         try:
#             details = self.service.get_user_details(uid)
#             if details:
#                 self.view.show_user_summary(details)
#         except Exception as e:
#             QMessageBox.critical(self.view, "Błąd", f"Wystąpił problem podczas pobierania szczegółów:\n{e}")
#
#     def delete_user(self, uid):
#         try:
#             success = self.service.deactivate_user(uid)
#             if success:
#                 QMessageBox.information(self.view, "Sukces", "Użytkownik został dezaktywowany.")
#                 self.view.reset_summary()
#                 self.show_users()
#         except Exception as e:
#             QMessageBox.critical(self.view, "Błąd", f"Wystąpił błąd podczas dezaktywacji:\n{e}")

