class Matematyka:

    @staticmethod
    def dodaj(a, b):
        return a + b

    @staticmethod
    def odejmij(a, b):
        return a - b

wynik = Matematyka.dodaj(5, 6)
print(wynik)

wynik = Matematyka.odejmij(65, 89)

print(wynik)


class ConverterTemp:

    @staticmethod
    def to_farenheit(a):
        return a * 9/5 + 32

    @staticmethod
    def to_celsjusz(a):
        return (a - 32) * 5/9


tem_far = ConverterTemp.to_farenheit(36.6)
print(tem_far)

tem_cel = ConverterTemp.to_celsjusz(0)
print(tem_cel)

# assert == ConverterTemp.to_farenheit(36.6)

# class KalkulatorTemperatur:
#
#     @staticmethod

