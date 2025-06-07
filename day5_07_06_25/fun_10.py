import operator

from functools import reduce, lru_cache


def add(a, b):
    return a + b


# funkcja reduce

sum_all = reduce(add, [1, 2, 3])
print(f"Reduce [sum]: {sum_all}")

sum_all = reduce(lambda a, b: a + b, [1, 2, 3])
print(f"Reduce [sum]: {sum_all}")

product = reduce(lambda a, b: a * b, [1, 2, 3, 4])
print(f"Reduce [products]: {product}")


lista = [1, 2, 3, 45, 67, 78, 100, 200, 300]

sum_all = reduce(lambda a, b: a + b, list(map(lambda n: n * 2, list(filter(lambda n: n % 2 == 0, lista)))))
print(f"Reduce: ",  sum_all)

l_1 = [i for i in lista if i % 2 == 0]
print(l_1)
l_2 = [i * 2 for i in l_1]
print(l_2)
sum_all = reduce(lambda a, b: a + b, l_2)
print(sum_all)

product = reduce(operator.mul, l_2)
print(f" mull", product)

add = reduce(operator.add, l_2)
print("add ", add)

concat_str = reduce(operator.add, ["Python", "rocks"])
print(concat_str)

min_num = reduce(lambda a, b: a if a < b else b, l_2)
print(f"Najmniejsza {min_num}")

print(reduce(lambda a, b: bool(a and b), [0, 0, 1, 0, 0]))
print(reduce(lambda a, b: bool(a and b), [0, 0, 0, 0, 0]))
print(reduce(lambda a, b: bool(a or b), [0, 0, 1, 0, 0]))
print(reduce(lambda a, b: bool(a or b), [0, 0, 0, 0, 0]))


@lru_cache(maxsize=1000)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fib = fibonacci(5)
print(fib)
print(fibonacci.cache_info())
fib = fibonacci(10)
print(fibonacci.cache_info())
print(fib)

fibonacci.cache_clear()
print(fibonacci.cache_info())

