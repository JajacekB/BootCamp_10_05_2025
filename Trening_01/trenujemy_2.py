user = 'Jacek'
wiek = 54
wersja = 3.14573209857
liczba = 3920183593

print(user, type(user))
print(wiek, type(wiek))
print(wersja, type(wersja))
print(liczba, type(liczba))

print(111 * "+")

print("Czesć %s, masz teraz %d lat" %(user, wiek))

print("Witaj %(user)s, masz teraz %(wiek)d lat" % {"user": user, 'wiek': wiek})

print("Wiatj %(czlowiek)s, masz teraz %(ege)d lat. Miło cię widzieć %(czlowiek)s." % {'czlowiek': user, "ege": wiek})

print(f"Witaj {user}, masz teraz {wiek} latek. Miło Cię widzieć {user}")

print(111* "-")

print('Uywamy wersji Pythona %i' %3)
print('Uywamy wersji Pythona %f' %3)
print('Uywamy wersji Pythona %f' %3.14)
print('Uywamy wersji Pythona %.2f' %3.14)
print('Uywamy wersji Pythona %.1f' %3.14)
print('Uywamy wersji Pythona %.1f' %3.17)
print('Uywamy wersji Pythona %.0f' %3.14)
print('Uywamy wersji Pythona %.f' %3.54)

print(111 * "_")

x = 4.79
print("Liczba po zaokrągleniu = %.0f" % x)
print("liczba się nie zmieniła", x)

y = round(x)
print(y , type(y))
print(float(y))

z = 3.14273487539
print(round(z, 2))

print(f"Uzywamy wersji Pythona {wersja}")
print(f"Uzywamy wersji Pythona {wersja:.1f}")
print(f"Uzywamy wersji Pythona {wersja:.2f}")
print(f"Uzywamy wersji Pythona {wersja:.0f}")

print(111 *'-')

liczba = 8428946729856213895

print(liczba)

print(f"Duża liczba {liczba:,}")
print(f"Duża liczba {liczba:_}")

print(10 * ' ')

print(f"Duża liczba {liczba:,}".replace(",", "."))
print(f"Duża liczba {liczba:,}".replace(",", " "))

print(111 * '+')

tekst = "jeden dwa trzy cztery pięć"
print(tekst)
print(tekst.split())

print(10* " ")

tekst2 = "jeden, dwa, trzy, cztery, pięć"
print(tekst2, type(tekst2))

tekst_new = tekst2.split(",")
print(tekst_new, type(tekst_new))
tekst_new2 = tekst2.split(", ")
print(tekst_new2, type(tekst_new2))