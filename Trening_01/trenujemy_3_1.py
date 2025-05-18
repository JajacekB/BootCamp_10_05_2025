tupla1 = "Radek"
print(tupla1)
print(type(tupla1))

tupla2 = ("Radek")
print(tupla2)
print(type(tupla2))

tupla3 = ("Radek",)
print(tupla3)
print(type(tupla3))

tupla4 = "Radek",
print(tupla4)
print(type(tupla4))

tupla_names = "Radek", "Tomek", "Zenek", "Bartek"
print(tupla_names)
print(type(tupla_names))

temp = 36, 6
print(temp)
print(type(temp))

tupla_liczby1= 43, 55, 22.34, 11, 200
print(tupla_liczby1)
print(type(tupla_liczby1))
tupla_liczby2 = (43, 55, 22.34, 11, 200)
print(tupla_liczby2)
print(type(tupla_liczby2))

print(" ")

print(tupla_liczby2 [:3])
print(tupla_liczby2 [-3:-2])
print(tupla_liczby2 [::-1])
print(tupla_liczby2 [-1::-1])
print(tupla_liczby2 [::2])
print(tupla_liczby2 [::-2])

print(" ")

print(tupla_names)
print("Radek" in(tupla_names))

print(tupla_names.count("Zenek"))
print(tupla_names.index("Radek"))
print(sorted(tupla_names))
print(tupla_names)
print(sorted(tupla_names, reverse=True))
print(tupla_names)

print(" ")

a, b = 1, 2
print(f' {a=}, {b=}')
a, b = b, a
print(f' {a=}, {b=}')

print(type((1, 2)))

tup1 = (1, 2)
a, b = tup1
print(f" {a=}, {b=}")

tup2 = (1, 2, 3)
a, *b = tup2
print(f" {a=}, {b=}")

print("")

print(tupla_names)
name1, name2, *name3 = tupla_names
print(f" {name1 =}, {name2=}, {name3=}")
*name1, name2, name3 = tupla_names
print(f" {name1 =}, {name2=}, {name3=}")

print(" ")

tupla_zadanie = ("Ola", "Ania", "Ada", "Gabi", "Kasia", "Paulia")
i1, i2, *i3, i4 = tupla_zadanie
print(i1, i2, i3, i4)

print("Jeden", "Dwa", "Trzy", "Cztery")
print("Jeden", "Dwa", "Trzy", "Cztery", sep="")
print("Jeden", "Dwa", "Trzy", "Cztery", sep="=>")
print("Jeden", "Dwa", "Trzy", "Cztery", sep=":")
print("Jeden", "Dwa", "Trzy", "Cztery", sep=":", end="")
print("Dalszy tekst")
print("Radek")

print(10 * "-")
listr = list(tupla_names)
print(listr)
print(type(listr))
