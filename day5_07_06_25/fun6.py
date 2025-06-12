# funkcja, która oblicza średnią
from itertools import count


def srednia(name = None, *cyfry):
    print(cyfry)
    count = len(cyfry)
    suma = 0
    sum_p = sum(cyfry)
    try:
        for c in cyfry:
            suma += c
        avg = suma / count
        avg_p = sum_p /count
    except Exception as e:
        print("Błąd", e)
    else:
        print(f"Średnia dla ucznia {name} wynosi {avg}")
        print(f"Średnia dla ucznia {name} wynosi {avg_p}")
    finally:
        print("Następne obliczenie")

srednia()
srednia(5, 5, 5, 5, 5, 5, 5)

srednia("Radek", 3, 6, 1, 4, 3, 2, 1, 5, 5, 2, 4, 3, 2, 4)


