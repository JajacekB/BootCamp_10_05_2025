import numpy as np

arr = np.array([1, 2, 3])
result = arr + 10

print(result)

arr1 = np.array([1, 2, 3])
arr2 = np.array([[10], [20], [30]])

print(arr1)
print(arr2)
print(arr1.shape)
print(arr2.shape)

result = arr1 + arr2
print(result)

arr1 = np.array(([[1, 2, 3],[4, 5, 6]]))
arr2 = np.array([10, 20, 30])
print(arr1)
print(arr1.shape)
print(arr2)
print(arr2.shape)

result = arr1 + arr2
print(result)

arr1 = np.ones((4, 3, 2))
print(arr1)

arr2 = np.array([10, 20])
print(arr2)

result = arr1 + arr2
print(result)

arr1 = np.array([1, 2, 3])
arr2 = np.array([10, 20])
print(arr1.shape)
print(arr2.shape)

# result = arr1 + arr2   - ValueError

x = np.arange(5)
y = np.arange(3)

x = np.arange(5)
y = np.arange(3)

y = np.arange(3).reshape(3, 1)

print(y)

print(x.shape)
print(y.shape)
print(x + y)

print(np.zeros((3, 5)))

print(np.eye((3)))



