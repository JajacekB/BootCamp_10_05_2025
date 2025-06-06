print("\nProgram służy do prostych obliczeń matematycznych na dwóch liczbach")

while True:

    # wybor dzialania
    print("""\nWybierz działanie:
    1. Dodawanie
    2. Odejmowanie
    3. Mnożenie
    4. Dzielenie
    5. Koniec""")

    dzialanie = input("Twój wybór: ")

    if dzialanie == '5':
        print("Koniec programu.")
        break

    if dzialanie not in ('1', '2', '3', '4', '5'):
        print("Błędny wybór. Spróbuj ponownie.")
        continue

    # pierwsza liczba
    while True:
        a_input = input("Podaj pierwszą liczbę: ")
        try:
            a = float(a_input)
            break
        except ValueError:
            print("To nie jest poprawna liczba. Spróbuj jeszcze raz.")

    # druga liczba
    while True:
        b_input = input("Podaj drugą liczbę: ")
        try:
            b = float(b_input)
            break
        except ValueError:
            print("To nie jest poprawna liczba. Spróbuj jeszcze raz.")

    # obliczenia
try:
    match dzialanie:
        case '1':
            wynik = a + b
            print(f"{a} + {b} = {wynik}")
        case '2':
            wynik = a - b
            print(f"{a} - {b} = {wynik}")
        case '3':
            wynik = a * b
            print(f"{a} * {b} = {wynik}")
        case '4':
            wynik = a / b
            print(f"{a} / {b} = {wynik}")
except ZeroDivisionError:
    print("Błąd: Nie można dzielić przez zero.")
except Exception as e:
    print("Nieznany błąd:", e)