from PySide6.QtCore import Slot


class RentVehicleController():
    def __init__(self, session, view, current_role):

        self.session = session
        self.view = view
        self.current_role = current_role

