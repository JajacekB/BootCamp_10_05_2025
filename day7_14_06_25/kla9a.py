class Pojazd:
    def serwis(self):
        print("Serwisoswanie pojazdu")


class SamochodOsobowy(Pojazd):
    def serwis(self):
        print("Serwisowanie samochodu osobowego")


class SamochodDostawcvzy(Pojazd):
    def serwis(self):
        print("Serwis samochodu dostawczego")


class PojazdSluzbowy(Pojazd):
    def rejestracja_sluzbowy(self):
        print("Rejestracja pojazdu słuzbowego")


class SamochodSluzbowyOsobowy(SamochodOsobowy, PojazdSluzbowy):
    pass


car1 = SamochodSluzbowyOsobowy()
car1.serwis()
car1.rejestracja_sluzbowy()

