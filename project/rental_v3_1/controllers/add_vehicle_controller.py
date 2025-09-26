from PySide6.QtCore import Slot
from sqlalchemy.exc import IntegrityError

from services.id_generators import generate_vehicle_id
from models.vehicle import  Bike, Car, Scooter


class AddVehicleController():
    def __init__(self, session, view, role):

        self.session = session
        self.view = view
        self.role = role

        self.view.handle_vehicles_data.connect(self._handle_generate_vehicles)
        self.view.update_db_request.connect(self._update_database)


    @Slot(list)
    def _handle_generate_vehicles(self, vehicles_data):
        vehicles = []
        for data in vehicles_data:
            if data["type"] == "car":
                vehicle_id = generate_vehicle_id(self.session, "C")
                vehicle = Car(
                    vehicle_id=vehicle_id,
                    brand=data["brand"],
                    vehicle_model=data["model"],
                    cash_per_day=data["cash_per_day"],
                    size=data["size"],
                    fuel_type=data["fuel"],
                    individual_id=data["individual_id"],
                )
            elif data["type"] == "scooter":
                vehicle_id = generate_vehicle_id(self.session, "S")
                vehicle = Scooter(
                    vehicle_id=vehicle_id,
                    brand=data["brand"],
                    vehicle_model=data["model"],
                    cash_per_day=data["cash_per_day"],
                    max_speed=data["max_speed"],
                    individual_id=data["individual_id"],
                )
            elif data["type"] == "bike":
                vehicle_id = generate_vehicle_id(self.session, "B")
                vehicle = Bike(
                    vehicle_id=vehicle_id,
                    brand=data["brand"],
                    vehicle_model=data["model"],
                    cash_per_day=data["cash_per_day"],
                    bike_type=data["bike_type"],
                    is_electric=data["is_electric"],
                    individual_id=data["individual_id"],
                )
            try:

                self.session.add(vehicle)
                self.session.flush()
                vehicles.append(vehicle)

            except IntegrityError as e:
                self.session.rollback()



        self.view.show_vehicles_list(vehicles)

    def _update_database(self):
        try:
            self.session.commit()
            self.view.show_results(True, "Dane zostały zapisane do bazy.")

        except Exception as e:
            self.session.rollback()
            self.view.show_results(False, f"Nie udało się zapisać do bazy:\n{e}")



