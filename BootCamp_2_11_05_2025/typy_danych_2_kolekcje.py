# Kolekcje
from itertools import count

# Lista
lista = []
print(lista)
print(type(lista))
print(bool(lista))
print(10 * "-")

pusta_lista = list()
print(pusta_lista)
print(type(pusta_lista))
print(bool(pusta_lista))
print(10 * "-")

lista_2 = [10, 20, 30]
print(lista_2)
print(type(lista_2))
print(10 * "-")

lista_3 = [10.77, 30.66, 67, 15]
print(lista_3)
print(type(lista_3))
print(10 * "-")

lista_mieszana = [10, 5.2, "Oko", "Radek"]
print(lista_mieszana)
print(type(lista_mieszana))
print(10 * "-")

print(len(lista_mieszana))
print(10 * "-")

# dodawanie elementow do listy
lista.append("Radek")
lista.append("Maciek")
lista.append("Tomek")
lista.append("Zenek")
lista.append("Marta")
lista.append("Anna")
print(lista)
print(type(lista))
print(len(lista))
print(10 * "-")

print(lista[1])
print(lista[len(lista) - 1])
print(lista[ - 1])
print(lista[ - 5])
print(lista[ - 6])
print(10 * "-")

# print(lista[10]) list index out of range
print(10 * "-")

print(lista[0:3])
print(lista[:3])
print(lista[:2])
print(lista[1:3])
print(lista[-3:])
print(lista[-2:])
print(lista[-1:])
print(lista[-1:][0])
print(lista[-1][0])
print(lista[-1][0])
print(lista[:])
print(lista[2:5])
print(lista[2:])
print(lista[-3:0])
print(lista[0:-3])
print(lista[2:2])
print(lista[2:3])
print(lista[4:10])
print(lista[7:10])












