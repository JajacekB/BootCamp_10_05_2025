wiek = 54
rok = 2015
temp = 36.6

print(temp, type(temp))

print(wiek + rok)
print(wiek - rok)
print(wiek * rok)
print(wiek / rok)

print(rok // wiek)
print(10 // 3)

print(wiek % rok)
print(10 % 3)

wynik = wiek ** rok
print(wiek)
print(f"Wiek do potęgi roku=: {wynik:,}")
print(f"Długość =: {len(str(wynik))}")
print(type(wynik))
# print(wynik ** 2)

print(10 * " ")

print(0.2 + 0.8)
print(0.2 + 0.7)
print(0.1 + 0.2)

print(f'''
{wiek}
{temp}

''')

print(type(4 / 2))
print(4 / 2)

logiczna = True
print(type(logiczna))
print(logiczna)

print(int(logiczna))
print(int(False))

print(bool(111))
print(bool("Tomek"))
print(bool(-15))

print(bool(0))
print(bool(""))
print(10 * "")

x = None
print(x)

a = 14
b = 3

print(f'{a=}')
print(f'{b=}')
print(f"Wynik porównania {a} > {b} = {a > b}")
print(f"Wynik porównania {a} < {b} = {a < b}")
print(f"Wynik porównania {a > b = }")
print(f"Wynik porównania {a} <= {b} = {a <= b}")
print(f"Wynik porównania {a} >= {b} = {a >= b}")
print(f"Wynik porównania {a} == {b} = {a == b}")
print(f"Wynik porównania {a} != {b} = {a != b}")

print(10 * " ")

c = a ^ b
print(bin(a))
print(bin(b))
print(bin(c))

a = a ^ b
b = b ^ a
a = a ^ b

print(a)
print(b)

print(10 * "---")

my_str1 = "afsdkljvn"
my_str2 = "12345Jacek"

print(my_str1.isalpha())
print(my_str1.isalnum())
print(my_str1.isdecimal())
print(my_str1.isnumeric())
print(my_str1.islower())
print(my_str1.isupper())
print(my_str1.isidentifier())

print(10 * ' ')

print(my_str2.isalpha())
print(my_str2.isalnum())
print(my_str2.isdecimal())
print(my_str2.isnumeric())
print(my_str2.islower())
print(my_str2.isupper())
print(my_str2.isidentifier())

print(10 * "+++")

print(True and True)
print(True and False)
print(False and True)
print(False and False)

print(10 * " ")

print(True or True)
print(True or False)
print(False or True)
print(False or False)

print(10 * " ")

print(not True)
print(not False)

print(10 * " ")

print(True ^ True)
print(True ^ False)
print(False ^ True)
print(False ^ False)

print(10 * " ")

print(not (True or True))
print(not (True or False))
print(not (False or True))
print(not (False or False))
