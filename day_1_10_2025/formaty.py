user = "Jacek"
wiek = 54
wersja = 3.90001
print(type(wersja))

print("Witaj %s masz teraz %d lat" % (user, wiek))

formatted_tex = f"Witaj {user} masz teraz {wiek} lat. Miło cię widzieć {user}"
print(formatted_tex)


print("uzywamy wersji Pythona %i" % 3)
print("uzywamy wersji Pythona %f" % 3)
print("uzywamy wersji Pythona %f" % 3.9)
print("uzywamy wersji Pythona %.2f" % 3.9)
print("uzywamy wersji Pythona %.1f" % 3.9)
print("uzywamy wersji Pythona %.0f" % 3.9)

x = 3.99
print("Liczba %.f," % x )
print("Liczba się nie zmieniła", x)

x = 3.99
x = round (x, 2)

# print(liczba)

print(f"{user:>10}")
print(f"{user:<15}")
print(f"{user:^20}")

tekst = "jeden dwa trzy cztery"
print(tekst.split())

tekst2 = "jeden, dwa, trzy, cztery"
print(tekst2.split(", "))

print(tekst2.split(","))
