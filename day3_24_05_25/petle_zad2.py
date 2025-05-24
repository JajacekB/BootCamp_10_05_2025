dictionary = {'imie': "Radek", 'nazwisko': "Kowalski"}
print(dictionary)
print(type(di))

for i in dictionary:
    print(i)

for k in dictionary.keys():
    print(k)

for v in dictionary.values():
    print(v)

for i in dictionary.items():
    print(i)

for k, v in dictionary.items():
    print(k,v, sep="<=>")

for k, v in dictionary.items():
    print(k, v, sep=" : ")

