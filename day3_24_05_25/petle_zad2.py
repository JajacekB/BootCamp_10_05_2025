dictionary = {'imie': "Radek", 'nazwisko': "Kowalski"}
print(dictionary)
print(type(dictionary))

for i in dictionary:
    print(i)

print("-")

for k in dictionary.keys():
    print(k)

print('+')

for v in dictionary.values():
    print(v)

print('=')

for i in dictionary.items():
    print(i)

print('@')

for k, v in dictionary.items():
    print(k,v, sep="<=>")

print('%')

for k, v in dictionary.items():
    print(k, v, sep=" : ")

