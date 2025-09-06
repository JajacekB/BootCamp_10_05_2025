import numpy as np

arr = np.array([1, 2, 3, 4])
print(arr.dtype)

print(np.iinfo(np.int64).min)
print(np.iinfo(np.int64).max)

print(2 ** 10)

arr_str = np.array(['aplle', 'banana', 'cherry'])
print(arr_str.dtype)

print(111 * '=')

arr_own = np.array([1, 2, 3, 4], dtype="S")

print(arr_own.dtype)
print(arr_own)

arr_i4 = np.array([1, 2, 3, 4], dtype='i4')
print(arr_i4)
print(arr_i4.dtype)

# arr_err = np.array(['a', '2', "3"], dtype="i")

arr_float = np.array([1.1, 2.1, 3.1, 4.1])
print(arr_float)
print(arr_float.dtype)

print(np.finfo(np.float64))


print(arr)

print(arr.dtype)
newarr = arr.astype("i")
print(newarr.dtype)

new_arr = arr.astype(int)
print(new_arr)
print(new_arr.dtype)

arr_bool = np.array((1,0,3))
new_arr_bool = arr_bool.astype(bool)
print(new_arr_bool)
print(new_arr_bool.dtype)


arr_float_2 = np.array([1.2, 2.1, 3.3, 4.4, 5.5])
print(arr_float_2.dtype)
print(arr_float_2)

print("Konwersja na int32: ", arr_float_2.astype("int32"))
print("Konwersja na int32: ", arr_float_2.astype("int32").dtype)

print("Konwersja na float15: ", arr_float_2.astype("int16"))
print("Konwersja na float15: ", arr_float_2.astype("int16").dtype)

print("Konwersja na bool: ", arr_float_2.astype("bool"))
print("Konwersja na bool: ", arr_float_2.astype("bool").dtype)

print("Konwersja na U6: ", arr_float_2.astype("U6"))
print("Konwersja na U6: ", arr_float_2.astype("U6").dtype)

print("Konwersja na uint8:", arr_float_2.astype("uint8"))
print("Konwersja na uint8:", arr_float_2.astype("uint8").dtype)


