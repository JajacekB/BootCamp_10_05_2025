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

print(111 * "+")
print("New")
print(111 * "-")

my_dict5 = {"Name": "Radek", "ID": 12345, "DDB": 1991, "Address": "Warsaw"}
print(my_dict5)
print(my_dict5["DDB"])
print(my_dict5.get("DDB"))

# nadpisanie wartości dla klucza

my_dict5["DDB"] = "1980"
print(my_dict5)

my_dict5["Address"] = "Warsaw Centrum"
print(my_dict5)

dict1 = {"DDB": 1995}
print(dict1)
print(type(dict1))

# update słownik słownikiem

my_dict5.update(dict1)
print(my_dict5)

# dodanie klucza do słownika

my_dict5["Job"] = "Developer"
print(my_dict5)

dict2 = {'cpi': 3.14}
print(dict2)

# update słownika

my_dict5.update(dict2)
print(my_dict5)

# usunięcie elemneyu

print(my_dict5.pop("cpi"))
print(my_dict5)

# usunięcie ostatniego elementu
print(my_dict5.popitem())
print(my_dict5)

# usuniecie po kluczy

del my_dict5["ID"]
print(my_dict5)

# usuniecie wszystkich elmentów
my_dict5.clear()
print(my_dict5)

# usunięcie z pamięci
del my_dict5

print("")

# zamiana klucza

slownik = {"stary_klucz": "wartość"}
print(slownik)
slownik["nowy_klucz"] = slownik.pop('stary_klucz')
print(slownik)

# kopiowanie slownika

my_dict5 = {'Name': 'Radek', 'ID': 12345, 'DDB': 1995, 'Address': 'Warsaw Centrum', 'Job': 'Developer', 'cpi': 3.14}
my_dict5_copy_ref = my_dict5
print(id(my_dict5_copy_ref))
print(id(my_dict5))

my_dict5_copy = my_dict5.copy()
my_dict5.clear()

print(my_dict5)
print(my_dict5_copy_ref)
print(my_dict5_copy)
print(id(my_dict5))
print(id(my_dict5_copy_ref))
print(id(my_dict5_copy))

print('')

dict_small = {"x": 3}
dict_small.update([("y", 4), ("z", 7)])
# update listą krotek

print(dict_small)
print(dict_small.items())

# napisać program, który będzie działał jak słownik angielsko-polski
# wyświetla dostepne słowa
# pobiera słowo od uzytkownika
# wyświetla tłumaczenie

# imput() - pobiera dane od użtkownika
# odp = input("podaj imię")
# print((odp))

# slow_pol_ang = {"żółty": "yellow", "czerwony": "red", "czarny": "black", "zielony": "green"}
# print(f"Możesz przetłumaczyc takie kolory {slow_pol_ang.keys()}")
# odp = input("podaj kolor")
# # print(slow_pol_ang[odp.strip().lower()])     # można tak
# print(slow_pol_ang[odp.strip().casefold()])  # lepiej tak,
#
# print((f"{odp.strip().casefold()} to: {slow_pol_ang.get(odp.strip().casefold())}"))  # Najlepiej i poprawnie
# print((f"{odp.strip().casefold()} to: {slow_pol_ang.get(odp.strip().casefold(), "Nie ma w słowniku")}"))  # Najlepiej i poprawnie

# a = input("Podaj liczbę")
# print(a)
# print(type(a))
#
# b = input("Podaj kolejną liczbę")
# print("Wynik (konkatanacja):" a + b)
# print("Wynik na liczbach:" int(a) + int(b))
# a = float(input("Podaj liczbę"))
# a = float(input("Podaj kolejną liczbę"))

print(all(my_dict5_copy))

print(any(my_dict5_copy))
