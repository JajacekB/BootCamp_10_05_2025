import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client['przykładowa_baza']
kolekcja = db['uzytkownicy']

# kolekcja.insert_one(
#     {'imie': "Anna", "nazwisko": "Nowak", "wiek": 23},
# )

kolekcja.insert_many(
    [
    {'imie': "Anna", "nazwisko": "Nowak", "wiek": 23},
    {'imie': "Halina", "nazwisko": "Sporna", "wiek": 31, 'czas': datetime.datetime.now().strftime("%d/%m/%Y")},
    ]
)

for uzytkownik in kolekcja.find():
    print(uzytkownik)

# print(kolekcja.find_one({"imie": 'Jan'}))

client.close()