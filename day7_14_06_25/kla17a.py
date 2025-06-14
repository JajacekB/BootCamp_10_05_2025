# wyjątki custom

class MyException(Exception):
    def __init__(self, message):
        super().__init__(message)


# raise ZeroDivisionError("Nie dziel przez zero")
#
# raise MyException("Wyjątek od Jacka")

try:
    x = int(input("Podaj liczbę całkowitą dodatnią "))
    if x < 0:
        print("Liczba ma być większa od zera")
        raise MyException("Liczba musi być dodatnia")
except MyException:
    print("Wystąpił wyjątek MyException")
except ValueError:
    print("Wystąpił błąd wartości")
except Exception as e:
    print("Inny błąd", e)
else:
    print("Wprowadziłeś poprawną wartość x:", x)
finally:
    print("Wprowadź kolejną daną")


