import operator
import time
from functools import partial

import numpy as np



def measure_time(func):
    def wrapper(*args, **kwargs):
        stat_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - stat_time
        print(f"Czas wykonania funkcji {func.__name__}: {execution_time}")
        return result

    return wrapper


@measure_time
def my_wait():
    time.sleep(2)


@measure_time
def my_for_sum():
    suma = 0
    for i in range(15_000_000):
        suma += i
    print("Sum is: ", sum)


@measure_time
def my_sum_withauo_for():
    total = sum(range(15_000_000))
    print("Suma jest", total)


@measure_time
def my_sum_np():
    total = np.sum(np.arange(15_000_000), dtype=np.int64)
    print('Sum jest sobie: ', total)


lista = list(range(1_000_000))
@measure_time
def my_for_mul():
    l = []
    for i in lista:
        l.append(i * 2)


@measure_time
def my_for_with_map_nul():
    l_map = []
    l_map = list(map(lambda x: x * 2, lista))


@measure_time
def my_for_comprehension():
    l = [i * 2 for i in lista]


@measure_time
def my_with_operator():
    l_map = list(map(partial(operator.mul, 2), lista))


my_wait()
my_for_sum()
my_sum_withauo_for()
my_sum_np()
print(100 * "-")
my_for_mul()
my_for_with_map_nul()
my_for_comprehension()
my_with_operator()