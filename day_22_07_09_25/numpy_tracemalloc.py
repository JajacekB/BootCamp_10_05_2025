import tracemalloc
import numpy as np

# tracemalloc.start()
# list1 = list(range(10_000_000))
# list2 = list(range(10_000_000))
#
# current, peak = tracemalloc.get_traced_memory()
# tracemalloc.start()
#
# print(f"Current memory usage: {current / 1024 ** 2} MB")
# print(f"Peak memory usage: {peak / 1024 ** 2} MB")


tracemalloc.start()

array1 = np.arange(10_000_000, dtype=np.int64)
array2 = np.arange(10_000_000, dtype=np.int64)

current, peak = tracemalloc.get_traced_memory()
tracemalloc.start()

print(f"Current memory usage: {current / 1024 ** 2} MB")
print(f"Peak memory usage: {peak / 1024 ** 2} MB")
