import numpy as np

arr = np.array([[1,2,3],[4, 5, 6]])

for x in arr:
    print(x)


for x in arr:
    print(x)
    for y in x:
        print(y)

arr = np.array([[[1, 2],[3, 4]],[[5, 6],[7,8]]])

for x in np.nditer(arr):
    print(x)


arr = np.array([1, 2, 3])
for x in np.nditer(arr, flags=['buffered'], op_dtypes=["S"]):
    print(x)


arr = np.array([[1, 2, 3, 4,],[5, 6, 7, 8]])
for x in np.nditer(arr[:, ::2]):
    print(x)


arr = np.array([1, 2, 3])
for idx, x in np.ndenumerate(arr):
    print(idx, x)

arr = np.array([[1, 2, 3, 4,],[5, 6, 7, 8]])
for idx, x in np.ndenumerate(arr):
    print(idx, x)





