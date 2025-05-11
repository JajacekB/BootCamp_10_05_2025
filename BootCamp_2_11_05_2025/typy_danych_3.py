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
