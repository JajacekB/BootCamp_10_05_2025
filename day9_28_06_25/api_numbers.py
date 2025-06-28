import requests

url="http://numbersapi.com/random/year?json"

response = requests.get(url)
print(response)
data = response.json()
print(type(data))

print(data)

print("Co wieesz o roku:\n",data['text'].replace(str(data['number']), ""))
print(data["text"],)

user_answer = input("\n???: ")

if user_answer == str(data["number"]):
    print("Brawo!!!")
else:
    print("Słabo, zła odpowiedź!!!")

insects = 10000000000000000000
print(f"{insects:,}")