import random
import statistics
lista = [44, 55, 66, 777, 33, 22, 11, 33, 11]
print(lista)
print(type(lista))

zbior = set(lista)
print(zbior)
print(type(zbior))

lista2 = list(zbior)
print(lista2)
print(type(lista2))
lista2.remove(33)
print(lista2)

zb2 = set()
print(zb2)
print(type(zb2))

zb2.add(2)
zb2.add(3)
zb2.add(5)
zb2.add(5)
zb2.add(3)
print(zb2)

print(zbior)
zbior.add(33)
zbior.add(18)
zbior.add(18)
print(zbior)

print(" ")

print(zbior.pop())
print(zbior)

print(zbior.pop())
zbior.pop()
zbior.pop()
print(zbior)

print(sorted(zbior))
print(zbior)

zbior.remove((55))
zbior.remove((18))
print(f"Zbior po usunięciu: {zbior=}")
print(f"Zbior po usunięciu: {zbior}")

print(111 * "-")

zbior2 = {667, 11, 44, 18, 52, 22, 667, 62, 999}
print(zbior2)

zbior3 = {667, 11, 44, 18, 667, 62, 999}
print(zbior3)

print(zbior | zbior3)
print(zbior.union(zbior3))
print(zbior)
print(zbior3)

zbior4 = {8, 9, 10}
print(zbior3.union(zbior4))
print(zbior | zbior3 | zbior4)

print(" ")

print(zbior & zbior3)
print(zbior.intersection(zbior3))

print(" ")

print(zbior - zbior3)
print(zbior.difference(zbior3))
print(zbior3.difference(zbior))

print(111 * "-")

a = {1, 2, 3}
b = {3, 4, 5}
a.update(b)
print(a)

a = {1, 2, 3}
b = {2, 3, 4}
a.intersection_update(b)
print(f"Zbiór a został nadpisany {a=}")

frozen_c = frozenset({1, 2, 3})
print(frozen_c)
print(type(frozen_c))

lista_temp = [{2, 3}, {4,5}]
print(lista_temp)

# zbior_zly = {1, {2, 3}}

lista_dobra = {1, frozenset({2, 3})}
print(lista_dobra)

print(" ")

zb3 = {1, 2, 3, 4, 5, 6, 7, 8, 9}
print(sum(zb3))
print(max(zb3))
print(min(zb3))
print(len(zb3))
print(statistics.mean(zb3))
print(statistics.median(zb3))
print(statistics.mode(zb3))
print(sorted(zb3))
lista_3 = list(zb3)
print(f"5 losowych liczb ze zbiru {zb3} to ", random.choices(lista_3, k=5))
print(f"3 niepowtarzalne losowe liczby ze zbiru {zb3} to ", random.sample(lista_3, k=3))

print(" ")

a = {1, 2, 3, 4, 5}
b = {3, 4}
print(b.issubset(a))

krotka = tuple(zb3)
lista = list(zb3)

print(krotka)
print(7 in krotka)

print(lista)
print(10 in lista)




