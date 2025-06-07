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


# mapowanie
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


# filtrowanie

lista_parzysta = []
for i in lista:
    if i % 2 == 0:
        lista_parzysta.append(i)

print(lista_parzysta)

# filter()
print(f"Zastosowanie filter(): {list(filter(lambda x: x < 3, lista))}")
print(f"Zastosowanie lilter(): {list(filter(lambda x: x > 15, lista))}")


print(f"Zastosowanie filter(): {list(filter(lambda x: x > 15 and x < 200, lista))}")
print(f"Zastosowanie filter(): {list(filter(lambda x: 15 < x < 200, lista))}")
print(f"Zastosowanie filter(): {list(filter(lambda x: x % 2 ==0, lista))}")

list3 = ['one', 'TWO', 'three', 'FOUR']
print(f"Filtrujemy: {list(filter(lambda x: x.isupper(), list3))}")
print(f"Filtrujemy: {list(filter(lambda x: x.islower(), list3))}")

list4 = ['one', 'two2', 'three3', '88', '99', '102', '1.23']
numeric = list(filter(lambda x: x.isnumeric(), list4))
print(f"Numeric: {numeric}")

alpha = list(filter(lambda x: x.isalpha(), list4))
print(f"Alpha: {alpha}")

alphanum = list(filter(lambda x: x.isalnum(), list4))
print(f"Alphanum: {alphanum}")

mix = list(filter(lambda x: x.isnumeric() and not x.isalpha(), list4))
print(f"Mix: {mix}")

