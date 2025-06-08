# klasa dom
# pola prywatne: kolor, liczba okien, metraż
# metody do odczytu i zapisu tych pól
# dodać metodę prywatną __farba() - > "zabrakło farby"

class Home:
    """
    Klasa opisująca dom
    """

    def __init__(self, kolor, liczba_okien, metraz):
        """
        Metoda inicjacji
        :param kolor:
        :param liczba_okien:
        :param metraz:
        """
        self.__kolor = kolor
        self.__liczba_okien = liczba_okien
        self.__metraz = metraz


    def sprawdz_color(self):
        print(f" Mama taki {self.__koor}")

    def policz_okna(self):
        print(f" Mam tyle {self.__liczba_okien}")

    def podaj_metraz(self):
            print(f" Mam {self.__metraz} powierzchn")

    def pomaluj(self, nowy_kolor):
        odp = input("Podaj kolor ")
        self.__kolor = odp
        self.sprawdz_kolor

    def dorob_okien(self):
        odp = input("Podaj ilość okien ")
        self.__liczba_okien = odp


policz_okna()