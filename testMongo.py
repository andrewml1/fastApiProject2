from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://andrewml1:ludacris@cluster0.iwdoxtk.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:

    db = client.test
    collection = db.my_collection
    document = {"name": "Valentina", "age": 31, "email": "lvalen1122@example.com"}
    result = collection.insert_one(document)
    print("Inserted:", document['name'])

except Exception as e:
    print(e)