# wyjątki - bledy

# print(5/ 0)
# print("Dalsza część programu")

# należy przechwycić i obsłuzyc wyjątek

try:
    wynik = 90/3
    # print(5 / 0)
    # print("a" / 2)
    print(int("A"))
    # print KeyError("Błąd klucza"
except ZeroDivisionError:
    print("Nie dziel przez zero")
except TypeError:
    print("Błą typu")
except ValueError:
    print("Błąd wartości")
except Exception as e:
    print("Błąd", e)
else:
    print("Wynik:", wynik)
finally:
    print("Koniec obliczeń")

print("Dalsza część programu")

