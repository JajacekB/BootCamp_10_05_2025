# klasa dom
# pola prywatne: kolor, liczba okien, metraż
# metody do odczytu i zapisu tych pól
# dodać metodę prywatną __farba() - > "zabrakło farby"

class Dom:
    """
    Klasa opisująca Dom
    """

    def __init__(self, metraz, kolor, liczba_okien):
        self.__metraz = metraz
        self.__kolor = kolor
        self.__liczba_okien = liczba_okien

    def wyswietl_okna(self):
        print(f"Mam {self.__liczba_okien} okna/okien")

    def wyswietl_kolor(self):
        print(f"Mam {self.__kolor} kolor")

    def wyswietl_metraz(self):
        print(f"Mam {self.__metraz} m2 powierzchni")

    def zmien_okna(self):
        odp = int(input("Podaj liczbę okien "))
        self.__liczba_okien = odp
        self.wyswietl_okna()

    def zmien_kolor(self):
        odp = input("Podaj kolor ")
        self.__kolor = odp
        self.wyswietl_kolor()
        self.__farba()

    def zmien_metraz(self):
        odp = int(input("Podaj metraz "))
        self.__metraz = odp
        self.wyswietl_metraz()

    def __farba(self):
        print("Zabrakło farby")

dom = Dom(168, "Beżowy", 17)
dom.wyswietl_metraz()
dom.wyswietl_kolor()
dom.wyswietl_okna()

dom.zmien_metraz()
dom.zmien_okna()
dom.zmien_kolor()