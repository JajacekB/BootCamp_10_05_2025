import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6])

newarr = np.array_split(arr, 3)
print(newarr)

newarr = np.array_split(arr, 4)
print(newarr)


arr = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
newarr = np.array_split(arr, 3)
print(newarr)

arr = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18]])
newarr = np.array_split(arr, 3, axis=1)
print(newarr)

arr = np.array([[[1, 2, 5], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]], [[19, 20, 21], [22, 23, 24], [25, 26, 27]]])
newarr = np.hsplit(arr, 3)
print(newarr)

newarr = np.vsplit(arr, 3)
print(newarr)

newarr = np.dsplit(arr, 3)
print(newarr)
