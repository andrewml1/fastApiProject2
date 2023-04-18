from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
#
# uri = "mongodb+srv://andrewml1:ludacris@cluster0.iwdoxtk.mongodb.net/?retryWrites=true&w=majority"
#
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
#
# # Send a ping to confirm a successful connection
# try:
#
#     db = client.test
#     collection = db.my_collection
#     document = {"name": "Andres",
#                 "age": 34,
#                 "email": "lvalen1122@example.com"}
#     result = collection.insert_one(document)
#     print("Inserted:", document)
#
# except Exception as e:
#     print(e)
#
# import csv
# import requests
#
# # Set the URL of your FastAPI endpoint
# url = "http://localhost:8000/Enviar"
#
# # Set the path of your CSV file
# csv_file = "data.csv"
#
# # Open the CSV file and read the records
# with open(csv_file) as f:
#     reader = csv.DictReader(f)
#     records = list(reader)

# Send the records to the API
for record in records:
    response = requests.post(url, json=record)
    print(response.json())
