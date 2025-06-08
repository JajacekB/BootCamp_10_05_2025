from abc import ABC, abstractmethod


class Ptak(ABC):
    """
    Klasa opisująca ptaka
    """

    def __init__(self, gatunek, szybkosc):
        """
        Metoda inicjaliujaca
        :param gatunek:
        :param szybkosc:
        """

        self.gatunek = gatunek
        self.szybkosc = szybkosc

    def latam(self):
        print("tu", self.gatunek, "Lecę", self.szybkosc )

    @abstractmethod
    def wydaje_odglos(self):

        """
        :return
        """


class Orzel(Ptak):
    """
    Klasa orzel
    """

    def wydaje_odglos(self):
        print("Kier kir kier")

    def polowanie(self):
        print("Tu", self.gatunek, "ja poluję")


class Kura(Ptak):
    """
    Klasa kura
    """

    def __init__(self,gatunek):
        super().__init__(gatunek, 0)

    def latam(self):
        print("Tu", self.gatunek, "Ja nie latam")

    def wydaje_odglos(self):
        print("Ko ko ko ko ")


class Sowa(Ptak):
    """
    Klasa Sowa
    """

or1 = Ptak("Orzeł", 45)
or1.latam()

kur1 = Ptak("Kura", 15)
kur1.latam()

kur2 = Kura("Kura")
kur2.latam()

# or2 = Ptak("Bielik", 45)
# or2.wydaje_odglos()



