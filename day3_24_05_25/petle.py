import random
from itertools import zip_longest

# pętle
# for - pętla iteracyjna

for i in range(10): # od 0 do 9
    print(i)

for i in range(10):
    print(i, i, sep=":") #1:1
    print(i, i)


for i in range(10):
    print(i, end="")

print()
print("Koniec pętli, nowa linia")

for i in range(1, 20):
    print(i)

for i in range(5):
    print("komunikat")

print()

for _ in range(1, 5):
    print("komunikat")
    print(_)

my_string = "Radek"
for i in my_string:
    print(i)

print()

for i in range(len(my_string)):
    print(my_string[i])

print('')

lista_wynik = []
lista_kule = list(range(1, 50))
for _ in range(6):
    wyn = random.choice(lista_kule)
    # print(wyn)
    lista_wynik.append(wyn)
    lista_kule.remove(wyn)
print(lista_wynik)
lista_wynik.sort()
print(f"Dzisiaj wylosowano nastepujące wyniki : {lista_wynik}")

lista_wylosowanych = []
beben = list(range(50, 100))

for _ in range(6):
    kula = random.choice(beben)
    lista_wylosowanych.append(kula)
    beben.remove(kula)

lista_wylosowanych.sort()
print(f"Wygrywająca piątka to : {lista_wylosowanych}")

print()

for i in range(10):
    if i % 2 != 0:
        print(i, "nieparzysta")

print()

for i in range(10):
    if i % 2 == 0:
        print(i, "parzysta")

print()

for i in range(30):
    if i % 3 == 0:
        print(i, "podzielna na 3")

print()

## list comprehensions
list3 = [j for j in range(1, 10) if j % 2 == 0]
print(list3)

cyfry = [1, 2, 3, 4, 5]
cyfry_zdublowane = [i * 2 for i in cyfry]
print(cyfry)
print(f"Cyfry zdublowane to: {cyfry_zdublowane}")

print()

cyfry_parzyste = [i for i in range(1, 33) if i % 2 == 0]
print(cyfry_parzyste)

cyfry_parzyste = [i for i in range(0, 33, 2)]
print(cyfry_parzyste)

print()

cyfry_fikusne = [i for i in range(1, 198) if i % 7 == 0 and i >= 29]
print(cyfry_fikusne)

print()

zdanie = ["Hello", "fantastic", "world"]
print(zdanie)
duze_litery = [slowo.upper() for slowo in zdanie]
print(duze_litery)

print()

triangle = [t ** 3 for t in range(0, 17)]
print(triangle)

print()

for c in list3:
    if c == 2:
        c += 1
        print("Tylko jeśli c=2")
    print('Przy każdym przejściu pętli', c)

print()

imiona = ['Radek', "Tomek", "Zenek", "Zbyszek"]
for p in imiona:
    print(p)

print()

imiona = ['Radek', "Tomek", "Zenek", "Zbyszek"]
for p in range(len(imiona)):
    print(p, imiona[p])

print()

for p in imiona:
    print(imiona.index(p), p)

print("enumeracja")

## enumeracja

for i in enumerate(imiona):
    print(i)

print()

# rozpakowanie krotki

print()

for i, o in enumerate(imiona):
    print(i, o)

print()

for i, o in enumerate(imiona, start=1):
    print(i, o)

print()
print("Coś nowego")
print()

ludzie = ['Janek', "Radek", "Tomek", 'Marek']
wiek = [45, 40, 18, 23]

for i in range(len(ludzie)):
    print(ludzie[i], wiek[i])

print()

ludzie = ['Janek', "Radek", "Tomek", 'Marek', "Ania"]
wiek = [45, 40, 18, 23]

# for i in range(len(ludzie)):
#    print(ludzie[i], wiek[i])

print()

for i in zip(ludzie, wiek):
    print(i)

for l, w in zip(ludzie, wiek):
    print(l, w)

for i in enumerate(zip(ludzie, wiek)):
    print(i)

print()

for i, (l,w) in enumerate(zip(ludzie, wiek), start=1):
    print(i, l, w)

print()

a, b = (3, ("Marek", 23))
print(a, b)

c, d = ('Marek', 23)
print(c, d)
print((a, c, d))

a, (c, d) = (3, ('Marek', 23))

for i, (o, w) in enumerate(zip(ludzie, wiek), start=1):
    print(f"Numer: {i}, Imię: {o}, Wiek: {w}")

print()

zipped = zip_longest(ludzie, wiek, fillvalue="None")
print(zipped)
print(type(zipped))

for i in zipped:
    print(i)

print(111 * "-")
#
for o, w in zipped:
    print(o, w)

print(111 * "-")
zipped = zip_longest(ludzie, wiek, fillvalue="None")
zipped_tuple = tuple(zipped)
print(zipped_tuple)
for (o, w) in zipped_tuple:
    print(o, w)

print(30 * '*')

for o, w in zipped_tuple:
    print(o, w)

print()

for i in range(0, 10, 2):
    print(i)

for i in range(-10, 0, 2):
    print(i)

for i in range(10, 0, -2):
    print(i)

parzyste = [i for i in range(0, 10, 2)]
print(parzyste)

print()

pol_ang = {"żółty": "yellow", "czerwony": "red", "czarny": "black", "zielony": "green"}

print(pol_ang)

ang_pol = {}
for k, v in pol_ang.items():
    ang_pol[v] = k
print(ang_pol)

print()

print({v: k for k, v in pol_ang.items()})

#