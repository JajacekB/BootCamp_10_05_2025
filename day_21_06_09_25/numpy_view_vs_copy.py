import numpy as np

arr = np.array([1, 2, 3, 4, 5])
x = arr.copy()
arr[0] = 42

print(arr)
print(x)

print(id(x), id(arr))
print(x.base is arr)

arr = np.array([1,2,3,4,5])
x=arr.view()
arr[0] = 42

print(arr)
print(x)

print(id(x), id(arr))
print(x.base is arr)

arr = np.arange(10)
print(arr)

view = arr[2:5]
print(view)
view[0] = 99
print(arr)
print(view)

print(view.base is arr)

arr = np.arange(10)
copy = arr[::2]
copy[0] = 99
print(copy)
print(arr)

print(copy.base in arr)

arr = np.arange(1000)
copy = arr[::2]
copy[0] = 67
print(copy[0])
print(arr[0])
print(copy.base is arr)

# arr = np.arange(1, 12).reshape(3, 4)
# print(arr)

view_col = arr[: 1].view()
print(view_col)
view_col[:] = 99
print(arr)

copy_row = arr[0 :].copy()
copy_row[:] = 0
print(arr)

print(copy_row)

print(copy_row.base is arr)

view_submatrix = arr[:2 :2].view()
view_submatrix *= 10
print(view_submatrix)

print(arr)

lista = [1, 2, 3, 4, 5]
print(lista * 2)
lista_slice = lista[1:3]
print(lista_slice)
lista_slice[0] = 99
print(lista)
print(lista_slice)


arr_1d = np.arange(10)
view_reversed = arr_1d[::-1].view()
view_reversed[0] = 999
print(arr_1d)
print(view_reversed)
print(view_reversed.base is arr_1d)

arr_3d = np.arange(27).reshape((3, 3, 3))
print(arr_3d)
copy_3d = arr_3d.copy()
copy_3d[0,0,0] = -1
print(copy_3d[0])
print(arr_3d[0])


print(copy_3d.base is arr_3d)

are_float = np.array([1.1, 2.2, 3.3, 4.4], dtype='float32')
print(are_float.dtype)
arr_view_as_int = are_float('int32').view()
print(are_float)
print(arr_view_as_int)
print(arr_view_as_int.dtype)
