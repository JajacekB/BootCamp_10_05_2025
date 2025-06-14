# class Person:
#     def __init__(self, first_name, last_name, id):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.id = id
#
#
# pl = Person("Jan", "Kowalski", 1)
# print(pl)
import pickle
from dataclasses import dataclass


@dataclass
class Person:
    first_name: str
    last_name: str
    id: int


p2 = Person("Jan", "Kowalski", 1)
print(p2)

p3 = Person("Maciej", "Nowak", 2)
print(p3)

people = [p2, p3]
print(people)

with open("dane.pickle", "wb") as stream:
    pickle.dump(people, stream)

