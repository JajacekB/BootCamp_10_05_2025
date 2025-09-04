from PySide6.QtCore import Slot

from services.vehicle_avability import get_available_vehicles


class RentVehicleController():
    def __init__(self, session, view, current_role):

        self.session = session
        self.view = view
        self.current_role = current_role

        self.view.handle_confirm_button.connect(self.get_vehicle_for_rent)

    @Slot(object, object, str)
    def get_vehicle_for_rent(self, start_date, planned_return_date, vehicle_type: str="all"):
        vehicles_to_rent = get_available_vehicles(
            self.session, start_date, planned_return_date, vehicle_type
        )

        self.view.show_vehicle_for_rent(vehicles_to_rent)

