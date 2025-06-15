import requests
from pydantic import BaseModel
from typing import List

url = "https://api.chucknorris.io/jokes/random"

response = requests.get(url)

print(response)
print(response.text)

print()

zarcik = response.json()
print(zarcik)
print(zarcik.keys())


print("Żartcik: ")
print(zarcik["value"])


class Joke(BaseModel):
    categories: list
    created_at: str
    icon_url: str
    id: str
    updated_at: str
    url: str
    value: str

joke = Joke(**zarcik)

print(joke)
print(joke.value)
print(joke.url)