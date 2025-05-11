# krotka (tupla) - kolekcja niemutowalna

tupla1 = "Jacek"
print(type(tupla1))

tupla2 = ("Jacek")
print(type(tupla2))

tupla3 = ("Jacek",) # lepiej tak bo więcej widać
print(type(tupla3))
print(tupla3)

tupla4 = "Jacek",
print(type(tupla4))
print(tupla4)

print(10 * "-")

tupla_names = "Radek", "Tomek", "Zenek", "Bartek"
print(type(tupla_names))
print(tupla_names)

temp = 36,6
print(type(temp))
print(temp)

tupla_liczby = 43, 55, 22.34, 11, 200
print(type(tupla_liczby))
print(tupla_liczby)
tupla_liczby = (43, 55, 22.34, 11, 200)
print(type(tupla_liczby))
print(tupla_liczby)

del temp
# print(temp)
print(10 * "-")

print(tupla_liczby)

print(tupla_liczby[1:4])
print(tupla_liczby[-4:-2])
print(tupla_liczby[::-1])

print(10 * "-")

print(tupla_liczby[-1])
print(tupla_liczby[::-1])
print(tupla_liczby[-1::-1])
print(tupla_liczby[1:4:2])
print(tupla_liczby[:])

print(10 * "-")

print(tupla_names)
print("Radek" in tupla_names)

print(tupla_names.count("Tomek"))
print(tupla_names.index("Tomek"))

print(10 * "-")

print(sorted(tupla_names)) # tworzy liste z tupli
print(tupla_names)

print(sorted(tupla_names, reverse=True))

print(10 * "-")

a, b = 1, 2
print(f"{a=}, {b=}")
b, a = a, b
print(f"{a=}, {b=}")

print(type((1, 2)))

tup1 = 1, 2
print(type(tup1))

a, b = tup1
print(f"{a=}, {b=}")

tup2 = 1, 2, 3
print(type(tup2))

# a, b = tup2 - nie zgadza sie rozmiar tupli

a, *b, = tup2
print(f"{a=}, {b=}")

print(10 * "-")

print(tupla_names)

a, b, c, d, = tupla_names
print(f"{a=}, {b=}, {c=} {d=}")

a, b, *c = tupla_names

*a, b, c
print(f"{a=}, {b=}, {c=}")

a, *b, c = tupla_names
print(f"{a=}, {b=}, {c=}")

print(10 * "-")

tupla_zadanie = "OLA", "Ania", "Ada", "Kasia", "Paulina"
i1, i2, *i3, i4 = tupla_zadanie
print(i1, i2, i3, i4)

print("Jeden", "Dwa", "Trzy")
print("Jeden", "Dwa", "Trzy", sep="")
print("Jeden", "Dwa", "Trzy", sep="=>")
print("Jeden", "Dwa", "Trzy", sep=":")
print("Jeden", "Dwa", "Trzy", sep=":", end="")
print("Dalszy tekst")
print("Radek")

print(10 * "-")

lista = list(tupla_names)
print(type(lista))
print(len(lista))
print(lista)

print(10 * "+")






