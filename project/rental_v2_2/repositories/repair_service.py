from datetime import date
from PySide6.QtWidgets import QMessageBox

from models.user import User
from models.repair_history import RepairHistory
from models.rental_history import RentalHistory
from services.id_generators import generate_repair_id
from services.rental_costs import calculate_rental_cost
from gui.windows.get_vehicle_widget import GetVehicleWidget
from gui.windows.repair_vehicle_widget import RepairVehicleWidget


repair_vehicle_widget = RepairVehicleWidget()
get_vehicle_widget = GetVehicleWidget()



def finalize_repair(session, vehicle, work_user, planned_return_date, total_cost, description):
    print("🔧 step 5a")

    repair_vehicle_widget.container_hbox0.hide()
    repair_vehicle_widget.container_hbox1.hide()
    repair_vehicle_widget.container_hbox2.hide()
    repair_vehicle_widget.container_hbox3.hide()

    repair_id = generate_repair_id(session)

    # Generowanie naprawy
    repair = RepairHistory(
        repair_id=repair_id,
        vehicle_id=vehicle.id,
        mechanic_id=work_user.id,
        start_date=date.today(),
        planned_return_date=planned_return_date,
        cost=total_cost,
        description=description)
    session.add(repair)

    # Aktualizacja pojazdu
    vehicle.is_available = False
    vehicle.borrower_id = work_user.id
    vehicle.return_date = planned_return_date

    try:
        session.commit()

        final_text_0 = " "
        final_text_1 = (
            f"Pojazd: {vehicle.brand} {vehicle.vehicle_model} {vehicle.individual_id}"
        )
        final_text_2 = (
            f"przekazany do warsztatu: {work_user.first_name} {work_user.last_name} do dnia {planned_return_date}."
        )
        get_vehicle_widget.vehicle_list.addItem(final_text_0)
        get_vehicle_widget.vehicle_list.addItem(final_text_1)
        get_vehicle_widget.vehicle_list.addItem(final_text_2)
        get_vehicle_widget.adjust_list_height()

    except Exception as e:
        session.rollback()
        QMessageBox.critical(
            None,
            "Błąd zapisu - naprawa",
            f"Nie udało się zapisać zmian w bazie.\n\nSzczegóły: {e}"
        )
    return True


def finish_after_vehicle_swap(session, vehicle, replacement_vehicle, different_price: bool):

    today = date.today()

    old_rental_cost = vehicle.rental.total_cost
    old_rental_period = (vehicle.rental.planned_return_date - vehicle.rental.start_date).days
    real_rental_days_old = (today - vehicle.rental.start_date).days
    real_rental_days_new = (vehicle.rental.planned_return_date - today).days

    if real_rental_days_old < 1:
        real_rental_days_old = 1
    if real_rental_days_new < 0:
        real_rental_days_new = 0

    # Oblicz koszt pojazdu zepsutego
    broken_veh_cost = old_rental_cost * real_rental_days_old / old_rental_period

    # different_price = False

    # Oblicz koszt pojazdu zastępczego
    if different_price:
        user = session.query(User).filter(User.id == vehicle.user_id).first()
        replacement_full_cost, _, _ = calculate_rental_cost(user, replacement_vehicle.cash_per_day, old_rental_period)
        replacement_partial_cost = replacement_full_cost * real_rental_days_new / old_rental_period

    else:
        replacement_veh_cost = old_rental_cost - broken_veh_cost

    # Aktualizacja statusu pojazdu zwracanego
    vehicle.is_available = True
    vehicle.borrower_id = None
    vehicle.return_date = None

    # Aktualizacja statusu pojazdu zastępczego
    replacement_vehicle.is_available = False
    replacement_vehicle.borrower_id = vehicle.rental.user_id
    replacement_vehicle.return_date = vehicle.rental.planned_return_date

    # Korekta historii najmu pojazdu popsutego
    vehicle.rental.actual_return_date = today
    vehicle.rental.total_cost = round(broken_veh_cost, 2)

    # Nowa rezerwacja dla pojazdu zastępczego
    base_res_id = vehicle.rental.reservation_id
    existing = session.query(RentalHistory).filter(
        RentalHistory.reservation_id.like(f"{base_res_id}%")
    ).all()

    new_suffix = chr(65 + len(existing))  # 'A', 'B', 'C', ...
    new_res_id = f"{base_res_id}{new_suffix}"

    new_rental = RentalHistory(
        reservation_id=new_res_id,
        user_id=vehicle.rental.user_id,
        vehicle_id=replacement_vehicle.id,
        start_date=today,
        planned_return_date=vehicle.rental.planned_return_date,
        base_cost=round(replacement_veh_cost, 2),
        total_cost=round(replacement_veh_cost, 2),
    )

    try:
        session.add(new_rental)
        session.commit()

        final_text_0 = " "
        final_text_1 = (
            f"Wydano pojazd zastępczy: {replacement_vehicle.brand} {replacement_vehicle.vehicle_model} "
            f"{replacement_vehicle.individual_id}"
        )

        get_vehicle_widget.vehicle_list.addItem(final_text_0)
        get_vehicle_widget.vehicle_list.addItem(final_text_1)
        get_vehicle_widget.adjust_list_height()

    except Exception as e:
        session.rollback()
        QMessageBox.critical(
            None,
            "Błąd zapisu",
            f"Nie udało się zapisać zmian w bazie.\n\nSzczegóły: {e}"
        )

    finalize_repair(session)
    return True