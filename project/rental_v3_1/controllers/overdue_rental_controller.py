from PySide6.QtCore import Slot, QDate

from services.rental_costs import recalculate_cost
from services.database_update import update_database
from repositories.write_methods import update_rental
from repositories.read_methods import overdue_tasks, get_user_by
from models.user import User
from models.rental_history import RentalHistory
from models.repair_history import RepairHistory


class OverdueRentalController():
    def __init__(self, session, view, role: str="seller"):

        self.session = session
        self.view = view
        self.current_role = role

        self.view.handle_overdue_tasks_details.connect(self.overdue_rental_details)
        self.view.handle_get_overdue.connect(self._get_overdue_tasks)
        self.view.handle_overdue_update_db.connect(self.overdue_update_db)


    def _get_overdue_tasks(self):
        overdues = overdue_tasks(self.session)

        if not overdues:
            self.view.show_no_overdue()

        else:
            self.view.overdue_action(overdues)

    @Slot(object)
    def overdue_rental_details(self, task):

        id_number = getattr(task, 'reservation_id', None) if isinstance(task, RentalHistory) else getattr(task,
            'repair_id', None)
        cost = getattr(task, 'total_cost', None) if isinstance(task, RentalHistory) else getattr(task, 'cost', None)

        id_user = getattr(task, 'user_id', None) if isinstance(task, RentalHistory) else getattr(task, 'mechanic_id', None)

        self.user = get_user_by(self.session, user_id=id_user)

        overdue_text = (
            f"Czy chcesz zakończyć?\n\n"
            f"ID: {id_number}\n"
            f"Pojazd: {task.vehicle.brand} {task.vehicle.vehicle_model}\n"
            f"Wynajęty/w naprawie od: {task.start_date.strftime('%d-%m-%Y')} "
            f"do: {task.planned_return_date.strftime('%d-%m-%Y')}\n"
            f"Do zapłaty: {cost} zł\n"
            f"Wynajęty przez: {self.user.first_name} {self.user.last_name}."
        )
        self.view.show_overdue_items_detail(overdue_text)

    @Slot(object, QDate)
    def overdue_update_db(self, task, actual_return_date_input):
        actual_return_date = actual_return_date_input.toPython()

        if isinstance(task, RepairHistory):
            success, msg = update_rental(self.session, task, actual_return_date)
            self.view.summary_update_repair(success, msg)

        elif isinstance(task, RentalHistory):

            total_cost, extra_fee, summary_text = recalculate_cost(
                self.session,
                self.user,
                task.vehicle,
                actual_return_date,
                task.reservation_id
            )

            update_database(
                self.session,
                task.vehicle,
                actual_return_date,
                total_cost,
                extra_fee,
                task.reservation_id
            )
            self.view.summary_rental(summary_text)