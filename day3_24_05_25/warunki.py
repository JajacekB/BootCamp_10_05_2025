# instrukcje warunkowe
# instrukcjie sterowania przepływem programu
# instrukcja if sterowana warunkiem
# if warunek:
#     komenda(blok) wykonany gdy warunek spełniony

odp = True
print((bool(odp))) # True
# odp = False
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

#suma_zam = 250
#if suma_zam > 150:
#    rabacik = 25
#else:
#    rabacik = 0
#
#print(f"Rabat wynosi {rabacik}")
#
#rabat = 250 if suma_zam > 150 else 0
#print(f"Rabat wynosi {rabat}")


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

# print("")
#
# alert_dict = {"console"; "Coś strasznego",
#             "email": {"error": "Krytyczny"},
#             "medium": "Ostrzeżenie"}
#
# if alert_system in alert_dict:
#     if alert_sytem == "conso;e":
#         print(alert_dict.get(alert_system))


# zrobić prpgram test z
# dodać punktację  (3 pytania)


biologia = {"ssak": "kot", "płaz": "żaba", "ptak": "bocian"}
punkty = 0

print(f" Podaj przykład ssaka")
ssak = "kot"
if ssak == biologia[ssak]:
    punkty += 1
else:
    punkty = punkty
płaz = "żaba"
if płaz == biologia[płaz]:
    punkty += 1
else:
    punkty = punkty


