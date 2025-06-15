# REST API - sposób komunikacji i wymiany danych: klient - server
# klient - np. przeglądarka
# server - backend
# korzysta z http
# metody - GET, POST, PUT/PATCH, DELETE - metody http


import requests
from pydantic import BaseModel
from typing import List



url = "http://api.open-notify.org/astros.json"


# uzyskamy czysty json
response = requests.get(url)
print(response)

print(response.text)
print(type(response.text))

# zamiana json na słownik
response_data = response.json()
print(type(response_data))
print(response_data)

print(response_data.keys())

for k in response_data:
    print(k)

people_list = response_data["people"]
for i in people_list:
    print(i)

alexander = people_list[6]["name"]
print(alexander)

class Astro(BaseModel):
    craft: str
    name: str

class AstroData(BaseModel):
    people: List[Astro]
    number: int
    message: str

print(111 * '+')

data = AstroData(**response_data)
print(data)

print(111 * '=')

print(data.number)
print(data.message)

print(111 * '*')

for p in data.people:
    print(p)

    print(p.__class__.__name__)
    print(f"{p.name=} {p.craft=}")
    print()

