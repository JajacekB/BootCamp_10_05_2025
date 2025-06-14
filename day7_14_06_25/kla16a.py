import pickle

dict = {
    "name": "Mariolka",
    "edge": 29,
    "citi": "Kraków"
}
with open("dict.pickle", "wb") as f:
    pickle.dump(dict, f)

with open("dict.pickle", "rb") as fn:
    read_dict = pickle.load(fn)

print(dict)
print(type(dict))

print(read_dict)
print(type(read_dict))

print("Gdzie mieszka:", read_dict["citi"])
print(read_dict["name"], "mieszka w", read_dict["citi"], "i ma", read_dict["edge"], "lat.")