# funkcje zwracajace wynik
# musza miec na końcu return

def odejmij(a, b):
    return a - b


def odejmij2(a=0, b=0, c=0):
    return a - b- c


def oblicz_vat(cena, vat=23):
    return cena * (100 + vat)/ 100


print(odejmij(6, 90))
wynik = odejmij(6, 90)
print("Wynik ", wynik)

print()

print(odejmij2())
print(odejmij2(5, 6))
print(odejmij2(5, 6, 4))
print(odejmij2(a= 6, b=7))
print(odejmij2(1, c = 8, b=5))

print()

print(odejmij2(6, 9) + odejmij2(100, 23, 6))

print()
print(oblicz_vat(1000))
print(oblicz_vat(1000, 8))
print(oblicz_vat(vat=15, cena=1000))

print()

vat1 = oblicz_vat(1000)
print(type(vat1))
print(vat1)

if vat1 == 1230:
    print("Działa")

