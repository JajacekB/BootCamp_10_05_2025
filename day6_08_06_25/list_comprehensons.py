# list comprehensions

numbers = [1, 2, 3, 4, 5]

# tworzenie nowej listy
squered = [num ** 2 for num in numbers]
print(f"Squred: {squered}")

even_numbers = [num for num in numbers if num % 2 == 0]
print(f"Even: {even_numbers}")

modifed_numbers = [num * 2 if num % 2 == 0 else num for num in numbers]
print(f"Zmodyfikowane: {modifed_numbers}")

even_odd = ['parzysta' if x % 2 == 0 else 'nieparzysta' for x in numbers]
print(f"Parzyste - Nieparzyste: {even_odd}")

numbers2 = [-2, -3, -4, -7]
absolute = [abs(x) for x in numbers2]
print(f"Wartości absolute: {absolute}")

word = "Python"
print(list(word))

letters = [letter for letter in word]
print(letters)

print([i for i in range(10)])
print([i for i in range(47)])
print([i for i in range(200) if i % 3 == 0 if i % 9 == 0 if i % 12 == 0])

