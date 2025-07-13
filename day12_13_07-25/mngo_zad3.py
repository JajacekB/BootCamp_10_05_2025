import certifi
from pymongo.server_api import ServerApi
from pymongo import MongoClient

url = "mongodb+srv://rajkonkret660:<db_password>@cluster0.pjuh61y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# client = MongoClient(url, server_api=ServerApi('1'))
client = MongoClient(url, server_api=ServerApi('1'), tlsCAFile=certifi.where())

try:
    client.admin.command('pong')
    print("Pinged Your development, You seccesfuly connected to Mongo")
except Exception as e:
    print("Error: ", e)


