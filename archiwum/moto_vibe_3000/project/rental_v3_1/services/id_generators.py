# directory: services
# file: id_generators.py

import re
from sqlalchemy import extract, func, cast, Integer
from database import SessionLocal
from models.rental_history import RentalHistory
from models.repair_history import RepairHistory
from models.invoice import Invoice
from models.vehicle import Vehicle


def generate_reservation_id(session):

    all_ids = session.query(RentalHistory.reservation_id).all()

    numeric_ids = []
    for (res_id,) in all_ids:
        if res_id and re.fullmatch(r"R\d+", res_id):
            numeric_ids.append(int(res_id[1:]))

    last_num = max(numeric_ids, default=0)
    new_num = last_num + 1

    digits = max(4, len(str(new_num)))
    return f"R{new_num:0{digits}d}"


def generate_repair_id(session):
    last = session.query(RepairHistory).order_by(RepairHistory.id.desc()).first()
    if last and last.repair_id and len(last.repair_id) > 1 and last.repair_id[1:].isdigit():
        last_num = int(last.repair_id[1:])
    else:
        last_num = 0
    new_num = last_num + 1

    digits = max(4, len(str(new_num)))
    return f"N{new_num:0{digits}d}"


def generate_invoice_number(session, planned_return_date):
    year = planned_return_date.year
    month = planned_return_date.month

    count = session.query(Invoice).filter(
        extract('year', Invoice.issue_date) == year,
        extract('month', Invoice.issue_date) == month
    ).count()

    sequence = count + 1

    invoice_number = f"FV/{year}/{month:02d}/{sequence:04d}"
    return invoice_number


def generate_vehicle_id(session ,prefix: str) -> str:
    prefix = prefix.upper()
    prefix_len = len(prefix)

    max_number_db = session.query(
        func.max(
            cast(func.substr(Vehicle.vehicle_id, prefix_len + 1), Integer)
        )
    ).filter(
        Vehicle.vehicle_id.ilike(f"{prefix}%")
    ).scalar() or 0

    max_number_pending = 0
    for obj in session.new:
        if isinstance(obj, Vehicle) and obj.vehicle_id and obj.vehicle_id.startswith(prefix):
            try:
                number = int(obj.vehicle_id[prefix_len:])
                if number > max_number_pending:
                    max_number_pending = number
            except ValueError:
                continue

    next_number = max(max_number_db, max_number_pending) + 1
    return f"{prefix}{next_number:03d}"