class Car:
    """
    Klasa opisująca samochód w Python
    """

    def __init__(self, model, year):
        """
        Metoda inicjacji
        :param model:
        :param year:
        """

        self.model = model
        self.year = year
        # hermetyzacja, pole prywatne
        self.__predkosc = 0

    def gaz(self):
        self.__predkosc += 20
        self.__zmien_bieg()

    def licznik(self):
        print(f"Prędkość wynosi: {self.__predkosc} km/h")

    def hamuj(self):
        self.__predkosc -= 10
        self.__zmien_bieg()

    def __zmien_bieg(self):
        print("Zmiana biegu")


car = Car("Opel", 2025)
car.licznik()
car.gaz()
car.gaz()
car.gaz()
car.gaz()
car.gaz()
# pole prywatne -nie ma dostepu poza klasą
# print(car.__predkosc)
car.licznik()
car.__predkosc = 0 # pole o tej samej nazwie ale globalne
car.licznik()
car.hamuj()
car.hamuj()
car.hamuj()
car.hamuj()
car.hamuj()
car.licznik()
car.hamuj()
car.hamuj()
car.hamuj()
car.hamuj()
car.hamuj()
car.licznik()

