# dziedziczenie
class Pojazd:
    def __init__(self, kolor):
        self.kolor = kolor

    def info(self):
        print(f"Kolor: {self.kolor}")


class Samochod(Pojazd):
    """
    Klasa Samochód, dziedziczenie po klasie Pojazd
    """
    def __init__(self, kolor, marka="Fiat"):
        """
        Metoda inicjalizacja
        :param kolor:
        :param marka:
        """
        super().__init__(kolor)
        self.marka = marka

    def info(self):
        super().info()
        print(f"Marka: {self.marka}")


class Rower(Pojazd):
    """
    Klasa Rower dziedziczy po klasie Pojazd
    """

poj = Pojazd("czerwone")
poj.info()

sam = Samochod("Biały")
sam.info()

sam2 = Samochod("Zielony", "Jaguar")
sam2.info()

rower = Rower("Zółty")
rower.info()

lista = [poj, sam, rower]
print(lista)