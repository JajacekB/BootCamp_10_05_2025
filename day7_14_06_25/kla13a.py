# ickle - serializacja i deserializacja obiektów
import pickle
import ast

lista = [1, 2, 3, 4, 5]

with open("lista.txt", "w") as f:
    f.write(str(lista))

with open("lista.txt", "r") as f:
    lines = f.read()

print(lines)
print(type(lines))

lista_odczytane_eval = eval(lines)
print(type(lista_odczytane_eval))
print(lista_odczytane_eval[0])

with open("lista.pickle", "wb") as f:
    pickle.dump(lista, f)

with open("lista.pickle", "rb") as fh:
    p = pickle.load(fh)

print(p)
print(type(p))
print(p[0])

list_ser = pickle.dumps(lista)
print(list_ser)

wynik = pickle.loads(list_ser)
print("Wynik deserializacji:", wynik)
print(wynik)
print(wynik[3])

user_input = "print('haked')"
eval(user_input)

lines = "[1, 2, 3, 4]"
lista = ast.literal_eval(lines)
print(lista)
print(type(lista))


