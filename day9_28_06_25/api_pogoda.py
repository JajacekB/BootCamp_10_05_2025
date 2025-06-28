import requests
from datetime import datetime

API_KEY="99a24a78addf" # klucz do podmiany

url = f"https://api.openweathermap.org/data/2.5/weather?q=Krakow&appid={API_KEY}&&lang=pl&format=jsonl&units=metric"

page = requests.get(url)
print(type(page))
print(page)
print(page.text)

data = page.json()
print(data)
print("Miasto: ", data["name"])
print("Pogoda: ", data["weather"][0]["description"])
print("Temperatura: ", data["main"]["temp"])
print("Tempratura minimalna: ", data["main"]["temp_min"])
print("Tempratura maxymalna: ", data["main"]["temp_max"])
print(111 * "-")
sunrise = data['sys']['sunrise']
print("Wschód słońca: ", ['sunrise'])

print("Tempratura minimalna: ", data["main"]["temp_min"])
dt_object_sunrise = datetime.fromtimestamp(sunrise)
print("Wschód słońca: ", dt_object_sunrise)

sunset = data['sys']['sunset']
dt_object_sunset = datetime.fromtimestamp(sunset)
print("Zachód słońca: ", dt_object_sunset)


