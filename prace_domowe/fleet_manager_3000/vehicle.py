# Program Fleet Manager 3000
# program służy do obsługi wypozyczlni ppojazdów.

from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(self, vehicle_id, brand, cash_per_day, is_available):
        """
        Konstruktor klasy abstrakcyjnej
        :param vehicle_id:
        :param brand:
        :param cash_per_day:
        :param is_available:
        """

        self.__id = vehicle_id
        self.__brand = brand
        self.__cash_per_day = cash_per_day
        self.__is_available = is_available

    @abstractmethod
    def get_type(self):
        pass

    def rent_car(self):
        """

        :return:
        """

    def return_car(self):
        """

        :return:
        """

    def __str__(self):
        return f"""ID: {self.__id}
    Marka: {self.__brand}
    Cena/dzień: {self.__cash_per_day} zł
    Dostępny: {self.__is_available}"""


class Car(Vehicle):
    def __init__(self, sits, engin):
        """

        :param sits:
        :param engin:
        """
        self.sits = sits
        self.engin =engin


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
