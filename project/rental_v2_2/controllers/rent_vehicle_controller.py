from sqlalchemy import func
from PySide6.QtCore import Slot

from models.vehicle import Vehicle
from models.invoice import Invoice
from models.rental_history import RentalHistory
from repositories.read_methods import get_user_by
from services.rental_costs import calculate_rental_cost
from services.vehicle_avability import get_available_vehicles
from services.id_generators import generate_reservation_id, generate_invoice_number


class RentVehicleController():
    def __init__(self, session, view, user):

        self.session = session
        self.view = view
        self.user = user

        self.view.handle_confirm_button.connect(self._get_vehicle_for_rent)
        self.view.handle_single_vehicle.connect(self._chose_single_vehicle)
        self.view.handle_accept_button.connect(self._accept_rent_chose)
        self.view.handle_rent_condition_accept.connect(self._accept_and_update_rental)

    @Slot(object, object, str)
    def _get_vehicle_for_rent(self, start_date, planned_return_date, vehicle_type: str= "all"):
        self.start_date = start_date
        self.planned_return_date = planned_return_date
        self.vehicle_type = vehicle_type

        vehicles_to_rent = get_available_vehicles(
            self.session, start_date, planned_return_date, vehicle_type
        )
        self.view.show_vehicle_for_rent(vehicles_to_rent)

    @Slot(list)
    def _chose_single_vehicle(self, group):

        matching_ids = [v.id for v in group]

        result = self.session.query(
            Vehicle,
            func.count(RentalHistory.id).label("rental_count")
        ).outerjoin(RentalHistory).filter(
            Vehicle.id.in_(matching_ids)
        ).group_by(Vehicle.id).order_by("rental_count").first()

        if result:
            self.chosen_vehicle, rental_count = result
        else:
            self.chosen_vehicle = group[0] if group else None
            rental_count = 0

        self.view.show_chosen_vehicle(self.chosen_vehicle, rental_count)

    @Slot(str)
    def _accept_rent_chose(self, client_info):
        if client_info:
            self.user = get_user_by(self.session ,user_id=client_info)

        print(f"{self.user}")

        rent_days = (self.planned_return_date - self.start_date).days
        self.base_cost = rent_days * self.chosen_vehicle.cash_per_day
        self.total_cost, discount_value, discount_type = calculate_rental_cost(
            self.session, self.user, self.chosen_vehicle.cash_per_day, rent_days
        )
        total_cost_str = (
            f"Całkowity koszt {self.total_cost} zł\n"
            f"Kwota bazowa {self.base_cost} zł, udzielone rabaty {discount_value} % {discount_type}"
        )
        self.view.show_rental_cost(self.total_cost, discount_value, discount_type, total_cost_str, self.user)

    @Slot(object)
    def _accept_and_update_rental(self, user: object=None):

        if user:
            self.user = user
        try:
            reservation_id = generate_reservation_id(self.session)
            invoice_number = generate_invoice_number(self.session, self.planned_return_date)

            self.chosen_vehicle.is_available = False
            self.chosen_vehicle.borrower_id = self.user.id
            self.chosen_vehicle.return_date = self.planned_return_date
            self.session.add(self.chosen_vehicle)

            rental = RentalHistory(
                reservation_id=reservation_id,
                user_id=self.user.id,
                vehicle_id=self.chosen_vehicle.id,
                start_date=self.start_date,
                planned_return_date=self.planned_return_date,
                base_cost=self.base_cost,
                total_cost=self.total_cost
            )
            self.session.add(rental)
            self.session.flush()

            invoice = Invoice(
                invoice_number=invoice_number,
                rental_id=rental.id,
                amount=self.total_cost,
                issue_date=self.planned_return_date
            )
            self.session.add_all([invoice])
            self.session.commit()

            success = True
            msg = (
                f"\n✅ Zarezerwowałeś {self.chosen_vehicle.brand} {self.chosen_vehicle.vehicle_model} "
                f"od {self.start_date} do {self.planned_return_date}."
                "\nMiłej jazdy!"
            )
            self.view.show_final_information(success, msg)


        except Exception as e:
            self.session.rollback()
            success = False
            msg = f"Wystąpił problem podczas zapisu rezerwacji.\nSzczegóły: {e}"

            self.view.show_final_information(success, msg)
