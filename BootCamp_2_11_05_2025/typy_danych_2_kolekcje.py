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

print(10 * "-")

#nadpisanie elementów w liście na wskazany indeks

lista[2] = "Mikołaj"
print(lista)
print(len(lista))

print(10 * "-")

# lista.insert(_index: 1, _object: ("Karolina"))
print(lista)
print(len(lista))

print(10 * "-")

# usunięcie po indeksie pop
print(lista.pop(0))
print(lista)
print(len(lista))
ind = lista.index("Zenek")
print("Numer dla indeksu Zenka", ind)
print(10 * "-")


lista.append("Zennek")
print(lista)
print("Numer dla indeksu Zenka", ind)
print(lista.pop(ind))
print(lista)

print("Numer dla indeksu Zenka", ind)

# Usunięcie po elemencie
lista.append("Maciek")
print(lista)
lista.remove("Maciek")
print(lista)

print(10 * "-")

print("Marta" in lista)
print("Marcin" in lista)

print(10 * "-")

print(lista.remove("Marta"))
print(lista)

lista.append("Marta")
lista.append("Marta")
lista.append("Marcin")
print(lista)
print(lista.index("Marta"))

print(10 * "-")

a = 1
b = 3
print(f"{a=}, {b=}")
a = b
print(f"{a=}, {b=}")
b = 7
print(f"{a=}, {b=}")

lista_4 = lista
print(f"{lista}")
print(f"{lista_4}")
lista_copy = lista.copy()
lista.clear()
print(f"{lista}")
print(f"{lista_4}")
print(f"{lista_copy}")

print(10 * "-")
# id()
print(f"adres: {id(lista)=}")
print(f"adres: {id(lista_4)=}")
print(f"adres: {id(lista_copy)=}")

print(10 * "-")

liczby = [45, 999, 34, 22, 13.34, 687]
print(liczby)
print(type(liczby))

liczby.sort()
print(liczby)
print(10 * "-")

liczby_a = [45, 999, 34, 22, 13.34, 687, "A"]
print(liczby_a)
print(type(liczby_a))

# liczby_a.sort()  not supported between instances of 'str' and 'int'

lista_osoby = ["Radek", "Tomek", "Zenek", "Ania", "Karolina", "Magda"]
lista_osoby.sort()
print(lista_osoby)

lista_alfabet = ["a", "z", "p", "d"]
lista_alfabet.sort()
print(lista_alfabet)
lista_alfabet_pol = ["a", "z", "ą", "p", "ń", "d"]
lista_alfabet_pol.sort()
print(lista_alfabet_pol)

print(ord("z"))
print(ord("ą"))

print(10 * "-")

# sortowanie i odwrocenie w 1 kroku
liczby.sort(reverse=True)
print(liczby)

#wypisanie w odwróconej kolejności bez zmiany bazowej listy
print(liczby[::-1])
print(liczby[0:4:2])
print(liczby)
print(liczby[-3:0:-1])

print(10 * "-")

# odwrócenie kolekcji bez sortowania
liczby_3 = [3, 8, 5, 12, 1]
liczby_3.reverse()
print(liczby_3)
print(10 * "-")

lista_osoby.reverse()
print(lista_osoby)

# laczenie list = nowa kolekcja

print(lista + liczby_a)
liczby_4 = liczby + liczby_3
print(liczby_4)

print(10 * "-")
print(liczby)

liczby[3] = 777
print(liczby)
liczby[-1] = 666
print(liczby)
print(liczby[1:4])
print(liczby[-4:-2])
usuniety = liczby.pop(2)
print(usuniety)
removniety = liczby.remove(22)
print(removniety)
print(liczby)
print(liczby[::-1])

print(10 * "-")

liczby_5 = [1, 2, 3, 4, 5]
liczby_6 = [6, 7, 8, 9]
liczby_5.extend(liczby_6)

print(liczby_5)

# rozpakowanie sekwencji
text = "Python"
# lista_str = lista(tekst)
print(lista)

print(10 * "-")
# lista_str2 = [tekst]
# print(lista_str2)

lista_str_pusta = []
# lista_str_pusta.extend(tekst)
print(lista_str_pusta)

lista_str_pusta = []
# lista_str_pusta.append(tekst)













