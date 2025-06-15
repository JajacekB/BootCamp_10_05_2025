import requests as re
from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime


url = "https://randomuser.me/api/"

response = re.get(url)
print(response)
print(response.text)
print(type(response))

data = response.json()

user = data['results'][0]

print(f"Osoba; {user['name']}")
print(f"Imie: {user['name']['first']}")
print(f"Nazwisko: {user['name']['last']}")

print(f"Numer telefonu: {user['phone']}")

user_name = user['name']['first']
user_last_name = user['name']['last']


photo_url = user['picture']['large']
print(f"Link do zdjęcia: {photo_url}")

response_photo = re.get(photo_url)
print(response_photo)

filename = f"{user_name.lower()}_{user_last_name.lower()}.jpg"
with open("fiename", "wb") as f:
    f.write(response_photo.content)

print(f"Zdjęciue zostało zapisane")


class Name(BaseModel):
    title: str
    first: str
    last: str


class Picture(BaseModel):
    large: HttpUrl
    midium: HttpUrl
    thumbnail: HttpUrl


class UserInfo(BaseModel):
    name: Name
    email: str
    picture: Picture


user = data['results'][0]
user_info = UserInfo(**user)
print(user_info)

print(f"Imie: {user_info.name.first}")
print(f"Nazwisko: {user_info.name.last}")

print((f"email: {user_info.email}"))

photo_url_Pydantic = user_info.picture.large
print(f"link do zdjęcia {photo_url_Pydantic}")

response_photo_pydantic = re.get(str(photo_url_Pydantic))
print(response_photo_pydantic)

filename = f"{user_name.lower}_{user_last_name.lower}.jpg"
with open(filename, "wb") as f:
    f.write(response_photo_pydantic.content)

    print("Zdjęcie zostało zapisane")