# stworzyć klasę pracownik
# imię, nazwisko, pensja
# metoda przedstaw_sie() oblicz_pensje()
# klasa menager metodą dzidziczenia pompracowniku
# co ma dzidziczyc a co ma nadpisać
from win32con import MF_ENABLED


class Pracownik:
    def __init__(self, imie, nazwisko, pensja):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pensja = pensja

    def przedstaw_sie(self):
        print(f"Nazywam się  {self.imie} {self.nazwisko}.")

    def oblicz_pensje(self):
        print(f"Zarabiam {self.pensja} zł.")



class Manager(Pracownik):
    def __init__(self, imie, nazwisko, pensja, premia):
        super().__init__(imie, nazwisko, pensja)
        self.premia = premia

    def oblicz_pensje(self):
        suma = self.pensja + self.premia
        print(f"zarabiam {suma} zł (w tym premia {self.premia} zł).")


p = Pracownik("Jagata", "Kwiecień", 5900)

p.przedstaw_sie()
p.oblicz_pensje()

m = Manager("Jantek", "Wrzesień", 8000, 3500)

m.przedstaw_sie()
m.oblicz_pensje()
