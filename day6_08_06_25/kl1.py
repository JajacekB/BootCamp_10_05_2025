# klasa - szablon, przepis
# 4 paradygmatu programowania
# 1 (enkapsulacja, hermetyzacja), 2 abstrakcja, 3 dziedziczenie, 4 polimorfizm
# obiekt - zbudowany wg. przepisu, instancja
# pola - zmienne
# metody - funkcje
# klasa musi być najpierw zadeklarowana
# tworzenie obiektu uruchamiania metodę __init__

# deklaracja klasy
# PascalCase
class Human:
    """
    Klasa Human opisująca człowieka w Pythonie
    """

    imie = ""
    wiek = None
    plec = "k"

    # self - obiekt
    def powitanie(self):
        print(f"Nazywam się {self.imie}")

    def stary(self):
        print(f"Mam {self.wiek} lat")


# tworzymy obiekt klas
cz1 = Human()
print(Human.__doc__)

# pydoc -b
# pydoc -w kl1
print(cz1.plec)
print(cz1.wiek)
print(cz1.imie)

cz1.plec = "m"
cz1.imie = "Janek"
cz1.wiek = 79

print(cz1.plec)
print(cz1.wiek)
print(cz1.imie)

cz2 = Human()
cz2.plec = "k"
cz2.imie = "Halinka"
cz2.wiek = 31

print(cz2.plec)
print(cz2.wiek)
print(cz2.imie)

cz1.powitanie()
cz1.stary()
cz2.powitanie()
cz2.stary()
