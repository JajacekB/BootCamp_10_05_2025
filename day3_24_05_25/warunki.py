# instrukcje warunkowe
# instrukcjie sterowania przepływem programu
# instrukcja if sterowana warunkiem
# if warunek:
#     komenda(blok) wykonany gdy warunek spełniony

odp = True
print((bool(odp))) # True
odp = False
if odp:
    print("Brawo")
    print("Brawo")
    print("Brawo")
    print("Brawo")
    print("Brawo")
    print("Brawo")
    print("Brawo")
    print("Brawo")

print("Dalsza część programu")

odp = "Radek"
if odp:
    print("ok")

odp = "Tomek"
if odp == "Radek":
    print("Radek")
else:
    print("inny pacjent")


# podatek = 0.9
# zarobki = int(input("Podaj dochód"))
# if zarobki < 30000:
#     podatek = 0.0
# elif zarobki < 60_000:
#     podatek = 0.2
# elif zarobki < 120_000:
#     podatek = 0.4
# else:   # działanie domyslne
#     podatek = 0.9
#
# print(f"Płacisz {zarobki * podatek} podatek")

suma_zam = 250
if suma_zam > 150:
    rabacik = 25
else:
    rabacik = 0

print(f"Rabat wynosi {rabacik}")

rabat = 25 if suma_zam > 150 else 0
print(f"Rabat wynosi {rabat}")


# zasymuluj system zbierania logów
# w zmiennej otrzymamy typ systemu: console, email, inny
# w zależności od zawartości zmiennej
# console -> "Stało się coś strasznego"
# email -> "System email"
# jeżeli będzie to system email to należy do listy błdów dodać opis
# druga zmienna prechowuje typ błędu
# error, medium,inny


system = "email"
blad = "error"
lista_bladow = []

if system == "console":
    print("Stało się coś strasznego")
elif system == "email":
    print("System email")
    if blad == "error":
        lista_bladow.append("Krytyczny")
        print("error")
    elif blad == "medium":
        lista_bladow.append("Ostrzeżenie")
        print("medium")
    elif blad == "inny":
        lista_bladow.append("Inny")
        print("inny")

else:
    print("Bład systemu")

print(lista_bladow)

print("")

alert_dict = {"console": "Coś poszło nie tak",
            "email": {"error": "Krytyczny", "medium": "Ostrzeżenie"}}

if system in alert_dict:
    if system == "console":
        print(alert_dict.get(system))
    elif system == "email":
        print("System email")
        print(alert_dict.get(system))
        if blad in alert_dict[system]:
            bledy = alert_dict[system]
            print(bledy[blad])
else:
    print("Inny System")


# # zrobić prpgram test z
# # dodać punktację  (3 pytania)
#
#
punkty = 0
odp = input("Podaj datę Chrztu Polski: ")
if odp == "966":
    punkty += 1
    print("Odpowiedź poprawna, zdobywasz punkt")
else:
    print("Źle")

odp = input("Na jakim kontynęcie leży Nepal: ")
if odp == "Azja":
    punkty += 1
    print("Odpowiedź poprawna, zdobywasz punkt")
else:
    print("Źle")

odp = input("Co to za ryba z wąsami: ")
if odp == "Sum":
    punkty += 1
    print("Odpowiedź poprawna, zdobywasz punkt")
else:
    print("Źle")

print(f"Zdobyłeś {punkty} punkty")

