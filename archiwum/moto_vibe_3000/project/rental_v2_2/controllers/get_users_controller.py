# get_users_controller.py
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QMessageBox

class GetUsersController:
    def __init__(self, view, service):
        self.view = view
        self.service = service

        self.view.handle_search_clicked.connect(self._on_search_clicked)
        self.view.handle_item_clicked.connect(self.on_item_clicked)

    @Slot()
    def _on_search_clicked(self):
        self.view.list_widget.clear()
        users_type = self.view.status_combo_box.currentText()

        success = True
        message = ""
        formatted_users = []

        try:
            if users_type == "Z wypożyczeniem":
                users = self.service.get_users_with_rent()
                if not users:
                    success = False
                    message = "Obecnie żaden klient nie wypożycza pojazdów."
                else:
                    formatted_users = self.service.format_users(users)

            elif users_type == "Bez wypożyczenia":
                users = self.service.get_users_without_rent()
                if not users:
                    success = False
                    message = "Brak aktywnych klientów bez wypożyczenia."
                else:
                    formatted_users = self.service.format_users(users)

            elif users_type == "Nieaktywni":
                users = self.service.get_inactive_users()
                if not users:
                    success = False
                    message = "Brak nieaktywnych klientów."
                else:
                    formatted_users = self.service.format_users(users)

            else:
                users = self.service.get_all_clients()
                if not users:
                    success = False
                    message = "Brak klientów w bazie."
                else:
                    formatted_users = self.service.format_users(users)

        except Exception as e:
            success = False
            message = f"Wystąpił błąd podczas pobierania danych:\n{e}"

        self.view.show_users_list(formatted_users, success, message)

    @Slot(int)
    def on_item_clicked(self, uid):
        if uid is None:
            return
        rentals = self.service.show_user_details(uid)
        self.view.show_user_details(rentals)


