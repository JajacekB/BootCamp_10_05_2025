# json - typ danych para klucz - wartość

import json
from xml.etree.ElementTree import indent

from mypy.util import json_dumps

person_dict = {'name': 'Radek', 'age': 40, 'czy_pali': None}
print(type(person_dict))

with open('nasze_dane.json', "w") as f:
    json.dump(person_dict, f)

# beautify - upiększanie
with open("nasze_dane_b.json", "w") as file:
    json.dump(person_dict, file, indent=4)
# {
#     "name": "Radek",
#     "age": 40,
#     "czy_pali": null
# }

# posortowanie po kluczach
with open("nasze_dane_sort.json", "w") as f:
    json.dump(person_dict, f, indent=4, sort_keys=True )
# {
#     "age": 40,
#     "czy_pali": null,
#     "name": "Radek"
# }

with open('nasze_dane.json', "r") as f:
    data = json.load(f)

print(data)
print(type(data))
print(data['name'])

# zmiana słownika na json

json_text = json.dumps(data)
print(json_text)
print(type(json_text))

# json na słownik

dict_json = json.loads(json_text)
print(dict_json)
print(type(dict_json))
print(dict_json['name'])






