from PySide6.QtWidgets import QMessageBox

from repositories.write_methods import add_user


class RegisterUserController:


    def __init__(self, session, view, parent_dialog=None):
        self.session = session
        self.view = view
        self.admin_dialog = parent_dialog
        self.view.registration_finished.connect(self.on_registration_finished_widget)
        self.view.registration_cancelled.connect(self.on_registration_cancelled_widget)

    def on_registration_finished_widget(self, user):

        success, text = add_user(self.session, user)


        if success:
            if self.admin_dialog:
                QMessageBox.information(None, "Sukces", text)
                self.admin_dialog.clear_dynamic_area()
            else:
                self.view.close()
        else:
            QMessageBox.warning(None, "Niepowodzenie", text)




    def on_registration_cancelled_widget(self):
        print("❌ Rejestracja anulowana – czyszczenie dynamicznego obszaru (RegisterWidget).")
        self.view.clear_form()
