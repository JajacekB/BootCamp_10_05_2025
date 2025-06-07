# funkcja lambda
# skrócony zapis funkcji
# zwraca wynik
# funkcja anonimowa - deklaracja w miejscu wykonania
from sys import base_prefix

odejmij = lambda a, b: a - b
print(odejmij(6, 10))
print(odejmij(b=8, a=87))

addition = lambda a, b: a + b
print(addition(6, 7))
res = addition(7, 8)
print(f"Wynik dodawania {res}")

res = lambda *args: sum(args)
print(res(10, 20))

res = lambda **kwargs: sum(kwargs.values())
print(res(a=10, b=20))

product = lambda a, b: a * b
print(product(4, 5))


def product1(nums):
    total = 1
    for i in nums:
        total *=i
    return


res1= lambda **kwargs: product1(kwargs.values())
print(res1)


def my_func(n):
    return lambda a: a + n

add10 = my_func(10)
add20 = my_func(20)
add30 = my_func(30)

print(add10(5))
print(add20(5))
print(add30(5))


oblicz_vat = lambda cena, vat=23: cena * (100 + vat) / 100
print(oblicz_vat(1000))
print(oblicz_vat(1000, 8))


wiek = lambda x: "dziecko" if x < 10 else ("nastolatek" if x <18 else "dorosły")
print(wiek(9))
print(wiek(10))
print(wiek(17))
print(wiek(18))
print(wiek(25))

lista = [1, 2, 3, 45, 67, 78, 100, 200, 300]

lista_wyn = []
for i in lista:
    lista_wyn.append(i * 2)
print(lista_wyn)

print([i * 2 for i in lista])


def zmien(x):
    return x * 2


lista_wyn_f = []
for i in lista:
    lista_wyn_f.append(zmien(i))
print(lista_wyn_f)

print(f"Zastosowanie map(); {list(map(zmien, lista))}")


print(f"Zastosowanie map(); {list(map(lambda x: x * 2, lista))}")
print(f"Zastosowanie map(); {list(map(lambda x: x * 4, lista))}")
print(f"Zastosowanie map(); {list(map(lambda x: x * 3.67, lista))}")
