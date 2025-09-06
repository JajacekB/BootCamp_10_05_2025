import numpy as np

a = np.array(42)
print(a.ndim)

b = np.array([1, 2, 3, 4, 5])
print(b.ndim)

c = np.array([[1, 2, 3], [4, 5, 6]])
print(c.ndim)

d = np.array([[[1, 2, 3], [4, 5, 6,]], [[1, 2, 3], [4, 5, 6]]])
print(d.ndim)

arr = np.array([1, 2, 3, 4], ndmin=5)
print(arr)
print("Wymiar: ", arr.ndim)


print(b)
print(b[0])
print(b[2])

print(c)
print("Pierwszy wiers: ", c[0])
print("pierwszy wiersz, drugi element: ", c[0][1])
print(c[0, 1])

arr_10 = np.array(([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]))
print(arr_10[1,3])

arr_12_3d = np.array([[[1, 2, 3,], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])

print(arr_12_3d)

print(10 * '@')

print(arr_12_3d[0])

print(arr_12_3d[0,1])

print(arr_12_3d[0, 1, 2])

print(arr_10[1, -1])