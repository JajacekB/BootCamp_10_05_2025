

class Human:
    """
    Klasa Human opisująca człowieka w Pythonie
    """

    def __init__(self, imie, wiek, wzrost, plec="k"):
        """
        Metoda inicjalizująca (konstruktor)
        :param imie:
        :param wiek:
        :param wzrost:
        :param plec:
        """

        self.imie = imie
        self.wiek = wiek
        self.wzrost = wzrost
        self.plec = plec

    def powitanie(self):
        print(f"Nazywam się {self.imie}")

    def stary(self):
        print(f"Mam {self.wiek} lat")

    def ruszaj(self):
        if self.plec == "m":
            print("Własnie wyruszylem w drogę")
        if self.plec == "k":
            print("Właśnie wyruszyłam w drogę")

cz1 = Human("Ulijan", 56, 163, "m")

print(cz1.imie)
print(cz1.wiek)
print(cz1.wzrost)
print(cz1.plec)

cz2 = Human("JoAnna", 33, 167, )

print(cz2.imie)
print(cz2.wiek)
print(cz2.wzrost)
print(cz2.plec)

cz1.powitanie()
cz1.stary()
cz1.ruszaj()
cz2.powitanie()
cz2.stary()
cz2.ruszaj()
