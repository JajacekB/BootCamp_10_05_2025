generator_1 = [x for x in range(5)]
print(generator_1)
print(type(generator_1))

generator_2 = (x for x in [1, 2, 3, 4, 5])  # to jest generator!!!
print(type(generator_2))
print(generator_2)

print(next(generator_2))
print(next(generator_2))
print(next(generator_2))
print(next(generator_2))
print(next(generator_2))

def generator3():
    for x in [1, 2, 3, 4, 5]:
        yield x

g3 = generator3()
print(next(g3))
print(next(g3))
print(next(g3))
print(next(g3))

def gen4():
    i = 1
    while True:
        yield i * i
        i += 1

g4 = gen4()
print(next(g4))
print(next(g4))
print(next(g4))
print(next(g4))
print(next(g4))
print(next(g4))

def fibo():
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b

fib1 = fibo()
print(next(fib1))
print(next(fib1))
print(next(fib1))
print(next(fib1))
print(next(fib1))
print(next(fib1))
print(next(fib1))

def fibo_with_index(n):
    a, b = 0, 1
    for ind in range(n):
        yield ind, b
        a, b = b, a + b

fib2 = fibo_with_index(10)
print(next(fib2))
print(next(fib2))
print(next(fib2))
print(next(fib2))
print(next(fib2))
print(next(fib2))

for i, n in fibo_with_index(10):
    print(f"Pozycja {i}, element {n}")

fibo3 = fibo_with_index(10)
print(list(fibo3))

print(15 * "-")
for i in fibo3:
    print(i)
    list()

def counter(start=0):
    n = start
    while True:
        result = yield n
        print(result)
        if result == "STOP":
            break

        n += 1

c = counter(20)
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print(c.send("OK"))

try:
    print(c.send("STOP"))
except StopIteration:
    print("Koniec")

