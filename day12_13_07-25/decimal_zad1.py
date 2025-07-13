from decimal import Decimal, ROUND_HALF_UP

decimal_1 = Decimal("0.1")
decimal_2 = Decimal(0.1)
decimal_3 = Decimal(1)

print(decimal_1)
print(decimal_2)
print(decimal_3)

print(f"Decimal('0.1') == Decimal(0.1)? {Decimal('0.1') == Decimal(0.1)}")
print(f"Decimal('0.1') == Decimal('0.1')? {Decimal('0.1') == Decimal('0.1')}")
print(f"Decimal('1') == Decimal(1)? {Decimal('1') == Decimal(1)}")

a = Decimal('10.345')
b = Decimal("3.2")

add = a + b
print("Dodawanie:", add)

substract = a - b
print(substract)

divide = a / b
print("Dzielenie", divide)

print("liczba zaokrąglona do dwóch miejsc po przecinku: ")
add = add.quantize(Decimal('0.01'))
print("Daodawanie", add)

substract = substract.quantize(Decimal('0.1'))
print("Odejmowanie:", substract)

multiply = a * b
multiply = multiply.quantize(Decimal('0.1'))
print("Mnożenie:", multiply)

divide = divide.quantize(Decimal('0.1'))
print("Dzielenie:", divide)

print("Dodawanie zaokrąglone ROUND_HALF_UP")
add = a + b
print(add)
print()
add = add.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
print(add)

multiply = a * b
multiply = multiply.quantize(Decimal('0.01'))
print("Mnożenie ROUNDHALF_UP", multiply)

value = Decimal("5.456")
rounding_nearest_005 = (
                                value / Decimal('0.05')
                        ).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * Decimal("0.05")

print(rounding_nearest_005)

print(Decimal("1.01") + 9)

