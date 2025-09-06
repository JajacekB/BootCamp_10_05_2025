import numpy as np

print(np.__version__)

arr = np.array([1, 2, 3, 4, 5])
print(arr)
print(type(arr))

# 0-D
arr_0d = np.array(42)
print(arr_0d)
print(type(arr_0d))

# 1-D
arr_1d = np.array([1, 2, 3, 4, 5])
print(arr_1d)

# 2-D
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print(arr_2d)

# 3-d
arr_3d = np.array([[[1, 2, 3], [4, 5, 6,]], [[1, 2, 3], [4, 5, 6]]])
print(arr_3d)
print(arr_3d.ndim)
