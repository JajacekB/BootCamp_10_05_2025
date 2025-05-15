user = 'Jacek'
wiek = 54
wersja = 3.14
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

