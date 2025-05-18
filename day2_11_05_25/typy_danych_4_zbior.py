# zbiór (set) - przechowuja unikalne wartosci (brak dupikatów)
# zbior nie posiada indeksu - brak kolejności przy dodawaniu elementow

lista = [44, 55, 66, 777, 33, 22, 11, 33, 11]
print(type(lista))
print(lista)
zbior = set(lista)
print(type(zbior))
print(zbior)

lista2 = list(zbior)
print(lista2)
lista2.remove(33)
print(lista2)

zb2 = set()
print(zb2)
print(type(zb2))

print(10 * "+")
zb2.add(2)
zb2.add(3)
zb2.add(5)
zb2.add(5)
zb2.add(3)
print(zb2)
print(10 * "+")

print(zbior)
zbior.add(33)
zbior.add(18)
zbior.add(18)
print(zbior)

print(10 * "+")

print(zbior.pop())
print(zbior)
zbior.pop()
zbior.pop()
print(zbior)

print(10 * "+")
print(sorted(zbior))

zbior.remove(55)
zbior.remove(18)
print(f"Zbior pousunieciu: {zbior=}")
print(f"Zbior pousunieciu: {zbior}")

print(10 * "_")

zbior2 = {667, 11, 44, 18, 52, 22, 667, 62, 999}
print(zbior2)

zbior3 = {667, 11, 44, 18, 667, 62, 999}
print(zbior3)

# suma zbiorów

print(zbior | zbior3)

print(zbior.union(zbior3))
print(zbior)
print(zbior3)

zbior4 = {8, 9, 10}
print(zbior.union( zbior3, zbior4 ))

print(zbior | zbior3 | zbior4)

# Czesc wspolna

print(zbior & zbior3)
print(zbior.intersection(zbior3))

# róznica

print(zbior - zbior3)
print(zbior.difference(zbior3))
print(zbior3.difference(zbior))

#suma
a = {1, 2}
b = {2, 3}
a.update(b)
print(f"{a=}")

a = {1, 2, 3}
b = {2, 3, 4}
a.intersection_update(b)
print(f"{a=}")

# frozenset - zbior niemutowalny

frozen = frozenset([1, 2, 3])
print(frozen)
print(type(frozen))

lista_temp = [[2, 3], [4, 5]]
print(lista_temp)

nested_set = {1, frozenset({2, 3})}
print(nested_set)
print(10 *"_")
zb3 = {1, 2, 3, 4, 5, 6, 7, 8, 9}
print(sum(zb3))
print(max(zb3))
print(min(zb3))
print(len(zb3))
print(sorted(zb3))

print(10 *"_")

# czy zbiów be jest podzbiorem zbioru a

a = {1, 2, 3}
b = {1, 2}
print(b.issubset(a))

krotka = tuple(zb3)
lista = list(zb3)

print(krotka)
print(9 in krotka)

print(lista)
print(10 in lista)


