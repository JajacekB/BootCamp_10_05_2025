

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __str__(self):
        return f"Użytkownik: {self.username}, Email: {self.email}"


class Client(User):
    def __init__(self, username, email):
        super().__init__(username, email)
        self.rented_vehicles = []

    def rent_vehicle(self, vehicle):
        self.rented_vehicles.append(vehicle)


class Admin(User):
    def __init__(self, username, email):
        super().__init__(username, email)

    def add_vehicle(self, fleet_manager, vehicle):
        fleet_manager.add_vehicle(vehicle)