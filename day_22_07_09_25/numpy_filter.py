import numpy as np

arr = np.array([41, 42, 43, 44])
x = [True, False, True, False]

newarr = arr[x]
print(newarr)

arr = np.array([41, 42, 43, 44])
filtered_arr = []

for element in arr:
    if element >42:
        filtered_arr.append(True)
    else:
        filtered_arr.append(False)

newarr = arr[filtered_arr]
print(filtered_arr)
print(newarr)

arr = np.array([41, 42, 43, 44])
filtered_arr = arr > 42
newarr = arr[filtered_arr]
print(filtered_arr)
print(newarr)

arr = np.arange(21)
even = arr[arr % 2 == 0]
print("Parzyste", even)

arr = np.random.randint(0, 100, size=100)

mean_values = np.mean(arr)
print(mean_values)
greater_than_mean = arr[arr > mean_values]
print(greater_than_mean)

arr = np.array([1,2, np.nan, 4, np.nan, 6, 7])
print(arr)

filtered_arr = arr[~np.isnan(arr)]
print("Tablica bez NaN:", filtered_arr)

arr = np.random.random((5, 5))
print(arr)
print(arr.shape)

filtered_arr = arr[arr > 0.5]
print("Większa od 0.5", filtered_arr)





