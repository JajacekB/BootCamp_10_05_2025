import pickle
from dataclasses import dataclass
from kla14a import Person

# @dataclass
# class Person:
#     first_name: str
#     last_name: str
#     id: int


with open("dane.pickle", "rb") as file:
    p = pickle.load(file)

print(p)

for person in p:
    print(person.first_name)
    person.greet()
