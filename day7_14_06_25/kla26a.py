from decimal import Decimal, ROUND_HALF_UP

print(0.2 + 0.8)
print(0.2 + 0.7)
print(0.1 + 0.2)

print()

decimal_1 = Decimal("0.1")
decimal_2 = Decimal(0.1)
decimal_3 = Decimal(1)

print(decimal_1)
print(decimal_2)
print(decimal_3)


print(f"{decimal_1 == decimal_2}")
print(f"{decimal_1 == Decimal("0.1")}")
print(f"Decimal(1) == Decimal(1) {decimal_3 == Decimal("1")}")

a = Decimal('10.345')
b = Decimal("3.2")

add = a + b
print("Dodawanie;", add)
substract = a -b
print("Odejmowanie", substract)
multiply = a * b
print("Mnożenie:", multiply)
divade = a / b
print("Dzielenie", divade)

precyzja = Decimal("0.01")
print("Liczba zaokręglona do dwóch miejsc po przecinku")
add = add.quantize(precyzja)
print("Dodawanie:", add)
substract = substract.quantize(precyzja)
print("Odejmnowanie:", substract)
multiply = multiply.quantize(precyzja)
print("Mnożenie:", multiply)
divade = divade.quantize(precyzja)
print("Dzielenie:", divade)

divade = a/b
print("Dzielenie z ustawieniem zaokrąglenia", divade.quantize(precyzja, rounding=ROUND_HALF_UP))

value = Decimal("5.456")
rounding_nearest_005 = (value / Decimal("0.05")).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * Decimal("0.05")
print(rounding_nearest_005)
print(Decimal("1.01"))