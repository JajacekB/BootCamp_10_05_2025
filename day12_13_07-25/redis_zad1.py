# Baza danych Redis

import redis

r = redis.Redis()

# dodanie
r.set("name", "Radek")

# odczyt i zamiana z bitowego na bajtowy
wartosc = r.get('name')
print(wartosc)
print(wartosc.decode('utf-8'))

# usuniecie
# r.delete("name")

# sprawdzenie czy istnieje
czy_istnieje = r.exists('name')
print("Czy istnieje?", czy_istnieje)
print("Czy istnieje?", bool(czy_istnieje))


d = {
    True: "Klucz istnieje",
    False: "Klucz nie istnieje"
}
print("Czy istnieje?", d[bool(czy_istnieje)])


