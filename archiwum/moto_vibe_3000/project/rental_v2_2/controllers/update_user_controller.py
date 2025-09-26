from PySide6.QtCore import Slot

from repositories.read_methods import get_user_by
from repositories.write_methods import update_user


class UpdateUserController():
    def __init__(self, session, view, user):

        self.session = session
        self.view = view
        self.user = user

        self.view.handle_update_user_data.connect(self._update_data)
        self.view.handle_update_password_data.connect(self._update_password)

    @Slot(dict)
    def _update_data(self, summary_data):

        success, msg = update_user(self.session, self.user, summary_data)
        user = get_user_by(self.session, user_id=self.user.id)
        self.view.update_user_data_confirmation(success, msg, user)

    @Slot(dict)
    def _update_password(self, summary_data):

        success, msg = update_user(self.session, self.user, summary_data)
        self.view.update_password_confirm(success, msg)