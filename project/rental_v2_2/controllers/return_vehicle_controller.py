
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtWidgets import QMessageBox

from services.rental_costs import recalculate_cost
from services.database_update import update_database
from repositories.return_vehicle_service import ReturnVehicleService


class ReturnVehicleController(QObject):
    operation_success = Signal(str)
    operation_error = Signal(str)

    def __init__(self, session, view=None, service=None, user=None):
        super().__init__()
        self.session = session
        self.view = view
        self.service = service
        self.user = user


        self.view.handle_rentals_list.connect(self.on_handle_rentals)
        self.view.handle_rental_detail.connect(self.get_rental_details)
        self.view.handle_end_rental.connect(self.get_rental_cost)
        self.view.handle_finalize_rental.connect(self.update_rental_data)

    def on_handle_rentals(self, mode: str):

        rentals = self.service.get_rentals_from_db(mode)
        self.view.load_rentals(rentals)

    def get_rental_details(self, rental):

        if rental is None or rental.actual_return_date is not None:
            return None
        self.rental = rental

        details = {
            "reservation_id": rental.reservation_id,
            "vehicle": f"{rental.vehicle.brand} {rental.vehicle.vehicle_model}",
            "start_date": rental.start_date,
            "end_date": rental.actual_return_date or rental.planned_return_date,
            "total_cost": rental.total_cost
        }
        self.view.show_rental_details(details)

    def get_rental_cost(self, vehicle, actual_return_date_input, reservation_id):
        self.total_cost, self.extra_fee, summary_text = recalculate_cost(
            self.session, self.user, vehicle, actual_return_date_input, reservation_id
        )
        self.actual_return_date_temp = actual_return_date_input
        self.vehicle = vehicle
        self.view.end_rental(summary_text)

    def update_rental_data(self):
        try:
            update_database(
                self.session,
                self.rental.vehicle,
                self.actual_return_date_temp,
                self.total_cost,
                self.extra_fee,
                self.rental.reservation_id
            )
            self.operation_success.emit("Zwrot został pomyślnie zarejestrowany.")

        except Exception as e:
            self.operation_error.emit(f"Wystąpił błąd: {str(e)}")

