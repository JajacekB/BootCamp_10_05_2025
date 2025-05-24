import random
from operator import index

print(random.randint(1, 100)) # int 1 do 100
print(random.randrange(1,100)) # int 1 do 99
print(random.randrange(10)) # int od 0 do 9
print(random.random())  # float od 0 do 0.9999999
print(random.random() * 7) # float od 0 do 6.99999

lista = [5, 7, 45, 34, 56]

index = random.randrange(len(lista))
print(index, lista[index])

print(random.choice(lista))

print(111 * "+")

lista_kule = list(range(1, 50))
print(lista_kule)

wyn = random.choice(lista_kule)
print(wyn)
lista_kule.remove(wyn)

print(random.choices(lista_kule, k=6))
print(random.sample(lista_kule, k=6))
print(random.sample(lista_kule, 6))

