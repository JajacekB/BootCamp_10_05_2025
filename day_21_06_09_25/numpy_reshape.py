import numpy as np


arr = np.arange(1, 13)
print(arr)
print(arr.dtype)
print(arr.shape)

newarr = arr.reshape(4, 3)
print(newarr)
print(newarr.shape)

newarr = arr.reshape(2, 3, 2)
print(newarr)
print(newarr.shape)


# arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
# newarr = arr.reshape(3, 3)

newarr = arr.reshape(2, 2, -1)
print(newarr)
print(newarr.shape)


# arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
# newarr = arr.reshape(2, 2, 1)
# print(newarr)
# print(newarr.shape)

arr = np.arange(12)
print(arr)
newarr = arr.reshape(-1, 2)
print(arr)
print(newarr)


newarr = arr.reshape(3, -1)
print(newarr)
print(newarr.shape)


newarr_order_f = arr.reshape((3, 4), order="F")
print(newarr_order_f)


newarr_order_c = arr.reshape((3, 4), order="C")
print(newarr_order_c)