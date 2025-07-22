from fleet_database import Session
from fleet_models_db import Vehicle

with Session() as session:
    types = session.query(Vehicle.type).distinct().all()
    print("Typy w bazie:", types)