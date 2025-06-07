# funkcje
# należy zadeklarowac funkcję
# w miejscu deklaracji funkcja sie nie wykonuje

a = 8
b = 6


def dodaj():
    print(a + b)


def dodaj2(a, b):
    print(a + b)
    c = 7


def odejmij(a, b, c=0):
    print(a - b - c)


print(dodaj)
print(type(dodaj))
dodaj()

# argumenty po pozycji
dodaj2(113, 289)

odejmij(134, 24)
odejmij(134, 24, 10)

# argumenty po nazwie
odejmij(c=9, b=26, a=65)
odejmij(b=67, a=34)
dodaj2(b=98, a=54)

odejmij(1, c=90, b=87)
odejmij(1, b=76)
# argumenty nazwane muszą być po pozycyjnych
# odejmij(c=90, 40, 60)

print(111 * '*')
print(dodaj())

print(dodaj2(45, 68))
