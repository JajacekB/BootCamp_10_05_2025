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

for _ in range(1, 5):
    print("komunikat")
    print(_)

my_string = "Radek"
for i in my_string:
    print(i)

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


for i in range(10):
    if i % 2 != 0:
        print(i, "nieparzysta")

for i in range(10):
    if i % 2 == 0:
        print(i, "parzysta")

for i in range(30):
    if i % 3 == 0:
        print(i, "podzielna na 3")

## list comprehensions
#list3 = [j for j in range(1, 10) if j % 2 == 0]
#print(list3)
#
#for c in list3:
#    if c == 2:
#        c += 1
#        print("Tylko jeśli c=2")
#    print('Przy każdym przejściu pętli', c)
#
#imiona = ['Radek', "Tomek", "Zenek", "Zbyszek"]
#for p in imiona:
#    print(p)
#
#imiona = ['Radek', "Tomek", "Zenek", "Zbyszek"]
#for p in range(len(imiona)):
#    print(p, imiona[p])
#
#for p in imiona:
#    print(imiona.index(p), p)
#
## enumeracja
#
#for i in enumerate(imiona):
#    print(i)
#
#for i, o in enumerate(imiona, start=1):
#    print(i, o)
#
#ludzie = ['Janek', "Radek", "Tomek", 'Marek', "Ania"]
#wiek = [45, 40, 18, 23]
#
## for i in range(len(ludzie)):
##     print(ludzie[i], wiek[i])
#
#for i in zip(ludzie, wiek):
#    print(i)
#
#for l, w in zip(ludzie, wiek):
#    print(l, w)
#
#for i in enumerate(zip(ludzie, wiek)):
#    print(i)
#
#a, b = (3, ("Marek", 23))
#print(a, b)
#c, d = ('Marek', 23)
#print(c, d)
#print((a, c, d))
#
#a, (c, d) = (3, ('Marek', 23))
#
#for i, (o, w) in enumerate(zip(ludzie, wiek)):
#    print(f"Numer: {i}, Imię: {o}, Wiek: {w}")
#
#print()
#
#zipped = zip_longest(ludzie, wiek, fillvalue="None")
#print(zipped) # iterator
#print(type(zipped))
#
#for i in zipped:
#    print(i)
#
#print(111 * "-")
#
#for o, w in zipped:
#    print(o, w)
#
#print(111 * "-")
#zipped = zip_longest(ludzie, wiek, fillvalue="None")
#zipped_tuple = tuple(zipped)
#print(zipped_tuple)
#for (o, w) in zipped_tuple:
#    print(o, w)
#
#for i in range(0, 10, 2):
#    print(i)
#
#for i in range(-10, 0, 2):
#    print(i)
#
#for i in range(10, 0, -2):
#    print(i)
#
#parzyste = [i for i in range(0, 10, 2)]
#print(parzyste)
#
#pol_ang = {"żółty": "yellow", "czerwony": "red", "czarny": "black", "zielony": "green"}

#ang_pol = {}
#for k, v in pol_ang.items():
#    ang_pol[v] = k
#print(ang_pol)
#
## print({v: k for k, v in pol_ang()})
#