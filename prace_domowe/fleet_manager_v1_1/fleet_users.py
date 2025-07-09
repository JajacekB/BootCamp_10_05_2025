

class User:
    def __init__(self, user_name, login, email, password):
        self.user_name = user_name
        self.login = login
        self.email = email
        self.password = password
        self.rented_vehicles = []

    def __str__(self):
        return f"Użytkownik: {self.user_name}, Email: {self.email}"

    def rent_vehicles(self, vehicle):
        self.rented_vehicles.append(vehicle)

    def return_vehicles(self, vehicle):
        if vehicle in self.rented_vehicles:
            self.rented_vehicles.remove(vehicle)


class Admin(User):
    def __init__(self, login, password):
        super().__init__(user_name="Admin", login=login, email="admin@system.local", password=password)

    def add_vehicles(self, fleet_manager, vehicle):
        fleet_manager.add_vehicle(vehicle)

    def add_seller(self, seller):
        pass  # TODO

    def change_password(self, user):
        pass  # TODO

class Seller(User):
    def __init__(self, user_name, login, email, password):
        super().__init__(user_name, login, email, password)

    def add_vehicle(self, fleet_manager, vehicle):
        fleet_manager.add_vehicle(vehicle)

    def change_password(self, user):
        pass  #TODO


class Client(User):
    def __init__(self, user_name, login, email, password):
        super().__init__(user_name, login, email, password)

    def change_password(self, user):
        pass  # TODO

