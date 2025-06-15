import requests as re
from pydantic import BaseModel
from typing import List


url = "https://restcountries.com/v3.1/name/Poland"

response = re.get(url)
print(response.text)

data = response.json()
print(type(data))
print()
#print(data.keys())

print()

kraj = data[0]


print(f"Nazwa kraju: {kraj["name"]}")
print(f" Nazwa oficjalna: {kraj["name"]["official"]}" )


class Pol(BaseModel):
    official: str
    common: str

class NativeName(BaseModel):
    pol: Pol

class Name(BaseModel):
    common: str
    official: str
    nativeName: NativeName
    # nativeName: dict

class CountryInfo(BaseModel):
    name: Name
    capital: List[str]
    population: int

country_data = [CountryInfo(**data) for data in response.json()]

for country in country_data:
    print(country)


    print(type(country))
    print(country.name)

    print(country.name.common)
    print(country.name.official)

    print(country.population)

    print(country.capital)
    print(country.capital[0])


