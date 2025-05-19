my_dict = {"A": "one", 'B': 'two', 'C': 'three', 'D': 'four'}
print(my_dict)
print(type(my_dict))

print(' ')

empty_dict = dict()
print(empty_dict)
print(type(empty_dict))

empty_dict2 = {}
print(empty_dict2)
print(type(empty_dict2))

print(" ")

dict_with_intiger = {1: 'one', 2: 'two', 3:'three'}
print(dict_with_intiger)

print(" ")

dict_mixed = {1: 'one', "B": 'two', 3: 'three'}
print(dict_mixed)

print(" ")

print(dict_mixed.keys())
print(dict_mixed.values())
print(dict_mixed.items())

print(" ")

dict_with_list = {1: 'one', 2: 'two', 'A': ['Asif', 'John', 'Maria']}
print(dict_with_list)

dict_with_list_and_tuple = {
    1: 'one',
    2: 'two',
    'A': ['Asif', 'John', 'Maria'],
    'b': ('Bat', 'Cat', 'Dog')
}
print(dict_with_list_and_tuple)
print(dict_with_list_and_tuple.values())
print(dict_with_list_and_tuple.keys())

print(' ')

dict_with_all = {
    1: 'one',
    2: 'two',
    'A': ['Asif', 'John', 'Maria'],
    "B": ('Bat', 'Cat', 'Dog'),
    "C": {'Name', 'age', 10}
}
print(dict_with_all)
print(dict_with_all.items())

print(" ")

dict_with_dict = {
    1: 'one',
    2: 'two',
    'A': ['Asif', 'John', 'Maria'],
    "B": ('Bat', 'Cat', 'Dog'),
    "C": {'Name', 'age', 10},
    "D": {"Name": 'Jacek', 'ege': 53}
}
print(dict_with_dict)

print(111 * "_")

keys = {'a', 'b', 'c', 'd'}
my_dict_from_keys = dict.fromkeys(keys)
print(my_dict_from_keys)

print(' ')

value = 10
my_dict_3 = dict.fromkeys(keys,value)
print(my_dict_3)

print(' ')

value = [10, 20, 30]
my_dict_4 = dict.fromkeys(keys, value)
print(my_dict_4)

print('')

keys = [1, 2, 2, 3, 4, 4, 5]
dict_unique = dict.fromkeys(keys)
print(dict_unique)
list_unique = list(dict_unique)
print(list_unique)

print(list(dict.fromkeys(keys)))

print(' ')

print(dict_with_dict["A"])

print(my_dict)
print(my_dict["A"])

print(dict_with_intiger[1])
print(dict_with_all["C"])
print(dict_with_all["A"])

print(my_dict_4.get("a"))
print(my_dict_4.get("e"))
print(my_dict_4.get('e', "Nie ma"))
print(my_dict_4.get('b', "Nie ma"))
