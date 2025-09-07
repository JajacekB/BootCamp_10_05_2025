import numpy as np

arr = np.arange(10)
print(arr)
print(arr.dtype)

arr = np.arange(5, 23)
print(arr)
print(arr.dtype)

arr = np.arange(0, 20, 2)
print(arr)
print(arr.dtype)

arr = np.arange(10, 0, -2)
print(arr)

arr = np.arange(0, 1, 0.1)
print(arr)

arr = np.arange(0, 5, dtype="float32")
print(arr)
print(arr.dtype)

arr = np.arange(1, 5, dtype="complex")
print(arr)
print(arr.dtype)

arr = np.arange(1, 5, 0.5)
print(arr)
print(arr.dtype)

arr = np.linspace(0, 1, 10)
print(arr)

arr = np.linspace(0, 1, 10, endpoint=False)
print(arr)

arr, step = np.linspace(0, 1, num=5, retstep=True)
print("Tablica:", arr)
print("krok:", step)

print(arr.shape)