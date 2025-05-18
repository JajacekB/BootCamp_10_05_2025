# slownik
# {'klucz' : "wartosc"}
# klucze nie mogą się powtarzac
# słownik jest odpowiednikiem jsona w python

my_dict = {"A": "one", "B": "two", "C": "three", "D": "four"}
print(my_dict)
print(type(my_dict))

empty_dict = dict()
print(empty_dict)

empty_dict2 = {}
print(empty_dict2)
print(type(empty_dict2))

dict_with_integer = {1: "one", 2: "two", 3: "three"}
print(dict_with_integer)

dict_mixet = {1: 'one', 'B': "two", 3: "three"}
print(dict_mixet.keys())
print(dict_mixet.values())
print(dict_mixet.items())

print(dict_with_integer.keys())

dict_with_list = {1: "one", 2: 'two', "A": ["asif", "john", "maria"]}
print(dict_with_list)

dict_with_list_and_touple = {
    1: 'one',
    2: 'two',
    "A": ["asif", "john", "maria"],
    "B": ('Bat', "cat", 'hat')
}
print(dict_with_list_and_touple)

#wypisanie wartości kluczy ze słaownika

print(dict_with_list_and_touple["A"])

print(dict_with_list_and_touple.get('e'))
print(dict_with_list_and_touple.get('e', "Nie ma"))
print(dict_with_list_and_touple.get('A', "Nie ma"))



