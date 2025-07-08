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

        self.__id = vehicle_id
        self.__brand = brand
        self.__cash_per_day = cash_per_day
        self.__is_available = is_available
        self.__borrower = borrower
        self.__return_date = return_date

    @abstractmethod
    def get_type(self):
        pass

    def rent_car(self, borrower, numer_of_days):
        if not self.__is_available:
            return False

        self.__is_available = False
        self.__borrower = borrower
        self.__return_date = date.today() + timedelta(days=numer_of_days)
        return True


    def return_car(self):
        if self.__is_available:
            return True

        self.__borrower = True
        self.__borrower = None
        self.__return_date = None

    def __str__(self):
        return f"""ID: {self.__id}
    Marka: {self.__brand}
    Cena/dzień: {self.__cash_per_day} zł
    Dostępny: {self.__is_available}
    Wypożyczył: {self.__borrower}
    Data zwrotu: {self.__return_date}
    """

    # konwersja obiektu klasy Vehicle do słownika dla późniejszego zapisu w pliku .json
    def to_dict(self):
        return {
            "id": self.__id,
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
    def __init__(self, vehicle_id, brand, cash_per_day, is_available, sits, engin):
        super().__init__(vehicle_id, brand, cash_per_day, is_available)
        self.sits = sits
        self.engin = engin


class Scooter(Vehicle):
    def __init__(self, max_speed):
        """

        :param max_speed:
        """
        self.max_speed = max_speed


class Bike(Vehicle):
    def __init__(self, category):
        """

        :param category:
        """
        self.type = category
