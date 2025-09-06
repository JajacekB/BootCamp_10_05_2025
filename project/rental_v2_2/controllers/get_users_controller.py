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

        try:
            if users_type == "Z wypożyczeniem":
                users = self.service.get_users_with_rent()
                if not users:
                    QMessageBox.information(self.view, "Informacja", "Obecnie żaden klient nie wypożycza pojazdów.")
                    return

            elif users_type == "Bez wypożyczenia":
                users = self.service.get_users_without_rent()
                if not users:
                    QMessageBox.information(self.view, "Informacja", "Brak aktywnych klientów bez wypożyczenia.")
                    return

            elif users_type == "Nieaktywni":
                users = self.service.get_inactive_users()
                if not users:
                    QMessageBox.information(self.view, "Informacja", "Brak nieaktywnych klientów.")
                    return

            else:
                users = self.service.get_all_clients()
                if not users:
                    QMessageBox.information(self.view, "Informacja", "Brak klientów w bazie.")
                    return

            for uid, user_str in self.service.format_users(users):
                self.view.add_user_to_list(uid, user_str)

        except Exception as e:
            QMessageBox.critical(self.view, "Błąd", f"Wystąpił błąd podczas pobierania danych:\n{e}")

    @Slot(object)
    def on_item_clicked(self, item):
        uid = item.data(Qt.UserRole)
        if not isinstance(uid, int):
            return

        try:
            details = self.service.get_user_details(uid)
            self.view.show_user_details(details)
        except Exception as e:
            QMessageBox.critical(self.view, "Błąd", f"Wystąpił błąd podczas pobierania szczegółów:\n{e}")