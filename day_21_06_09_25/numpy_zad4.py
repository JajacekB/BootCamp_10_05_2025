from time import process_time_ns

import numpy as np

lista = [1, 2, 3, 4, 5]
print(lista[2:4])

arr = np.array([1, 2, 3, 4, 5, 6, 7])

print(arr[1:5])
print(arr[4:])
print(arr[:4])
print(arr[-3:1])

print(arr[1:5:2])
print(arr[::2])

arr_10_2d = np.array([[1, 2, 3, 4, 5,], [6, 7, 8, 9, 10]])
print(arr_10_2d[1, 1:4])

print(arr_10_2d[0:2, 2])

print(arr_10_2d[0:2, 1:4])


arr_3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])

print(arr_3d)

print(arr_3d[0:2, 1:2, 0:1])