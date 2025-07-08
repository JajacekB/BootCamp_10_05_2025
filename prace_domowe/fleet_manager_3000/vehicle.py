# Program Fleet Manager 3000
# program służy do obsługi wypozyczlni ppojazdów.

from abc import ABC, abstractmethod
from datetime import date, timedelta, datetime

class Vehicle(ABC):
    def __init__(self, vehicle_id, brand, cash_per_day, is_available=True, borrower=None, return_date=None):
        """
        Konstruktor klasy abstrakcyjnej
        :param vehicle_id:
        :param brand:
        :param cash_per_day:
        :param is_available:
        :param borrower:
        :param return_date:
        """

        self.__vehicle_id = vehicle_id
        self.__brand = brand
        self.__cash_per_day = cash_per_day
        self.__is_available = is_available
        self.__borrower = borrower
        self.__return_date = return_date

    @abstractmethod
    def get_type(self):
        pass

    def rent(self, borrower, numer_of_days):
        if not self.__is_available:
            return False

        self.__is_available = False
        self.__borrower = borrower
        self.__return_date = date.today() + timedelta(days=numer_of_days)
        return True


    def return_vehicle(self):
        if self.__is_available:
            return True

        self.__is_available = True
        self.__borrower = None
        self.__return_date = None

    def __str__(self):
        return_date_str = self.__return_date.strftime("%Y-%m-%d") if self.__return_date else "brak"
        return f"""ID: {self.__vehicle_id}
    Marka: {self.__brand}
    Cena/dzień: {self.__cash_per_day} zł
    Dostępny: {self.__is_available}
    Wypożyczył: {self.__borrower}
    Data zwrotu: {return_date_str}
    """

    # konwersja obiektu klasy Vehicle do słownika dla późniejszego zapisu w pliku .json
    def to_dict(self):
        return {
            "id": self.__vehicle_id,
            "brand": self.__brand,
            "cash_per_day": self.__cash_per_day,
            "is_available": self.__is_available,
            "borrower": self.__borrower,
            "return_date": self.__return_date.strftime("%Y-%m-%d") if self.__return_date else None,
            "type": self.get_type()
        }

    # konwersja słownika (.json) do obiektu klasy Vehicle
    @classmethod
    def from_dict(cls, data):
        return cls(
            vehicle_id=data["id"],
            brand=data["brand"],
            cash_per_day=data["cash_per_day"],
            is_available=data["is_available"],
            borrower=data["borrower"],
            return_date=datetime.strptime(data["return_date"], "%Y-%m-%d").date() if data["return_date"] else None
        )




class Car(Vehicle):
    def __init__(self, vehicle_id, brand, cash_per_day, is_available, seats, fuel_type, borrower=None, return_date=None):
        super().__init__(vehicle_id, brand, cash_per_day, is_available, borrower, return_date)
        self.seats = seats
        self.fuel_type = fuel_type

    def get_type(self):
        return "Samochód"

    def __str__(self):
        return super().__str__() + f"""Liczba miejsc: {self.seats}
    Typ paliwa: {self.fuel_type}
    """

    # Konwersja obiektu klasy Car do słownika dla późniejszego zapisu w pliku .json z nadpisaniem klasy Vehicle
    def to_dict(self):
        data = super().to_dict()  # pobiera dane z Vehicle
        data.update({
            "seats": self.seats,
            "fuel_type": self.fuel_type
        })
        return data

    # Konwersja z .json do obiektu klasy Car
    @classmethod
    def from_dict(cls, data):
        return cls(
            vehicle_id=data["id"],
            brand=data["brand"],
            cash_per_day=data["cash_per_day"],
            is_available=data["is_available"],
            seats=data["seats"],
            fuel_type=data["fuel_type"],
            borrower=data["borrower"],
            return_date=datetime.strptime(data["return_date"], "%Y-%m-%d").date() if data["return_date"] else None
        )


class Scooter(Vehicle):
    def __init__(self, vehicle_id, brand, cash_per_day, is_available, max_speed, borrower=None, return_date=None):
        super().__init__(vehicle_id, brand, cash_per_day, is_available, borrower, return_date)
        self.max_speed = max_speed

    def get_type(self):
        return "Scooter"

    def __str__(self):
        return super().__str__() + f"Maksymalna prędkość: {self.max_speed}km/h\n"

    # Konwersja obiektu klasy Scooter do słownika dla późniejszego zapisu w pliku .json z nadpisaniem klasy Vehicle
    def to_dict(self):
        data = super().to_dict()  # pobiera dane z Vehicle
        data.update({"max_speed": self.max_speed})
        return data

    # Konwersja z .json do obiektu klasy Scooter
    @classmethod
    def from_dict(cls, data):
        return cls(
            vehicle_id=data["id"],
            brand=data["brand"],
            cash_per_day=data["cash_per_day"],
            is_available=data["is_available"],
            max_speed=data["max_speed"],
            borrower=data["borrower"],
            return_date=datetime.strptime(data["return_date"], "%Y-%m-%d").date() if data["return_date"] else None
        )


class Bike(Vehicle):
    def __init__(self,vehicle_id, brand, cash_per_day, is_available, bike_type, is_electric, borrower=None, return_date=None):
        super().__init__(vehicle_id, brand, cash_per_day, is_available, borrower, return_date)
        self.bike_type = bike_type
        self.is_electric = is_electric

    def get_type(self):
        return "Rower"

    def __str__(self):
        return super().__str__() + (f"""Typ roweru: {self.bike_type}
        Elektryczny: {'Tak' if self.is_electric else 'Nie'}\n""")

    def to_dict(self):
        data = super().to_dict()  # pobiera dane z Vehicle
        data.update({
            "bike_type": self.bike_type,
            "is_electric": self.is_electric
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            vehicle_id=data["id"],
            brand=data["brand"],
            cash_per_day=data["cash_per_day"],
            is_available=data["is_available"],
            bike_type=data["bike_type"],
            is_electric=data["is_electric"],
            borrower=data["borrower"],
            return_date=datetime.strptime(data["return_date"], "%Y-%m-%d").date() if data["return_date"] else None
        )