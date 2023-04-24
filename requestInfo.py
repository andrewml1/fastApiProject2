import requests

# Define the data to send in the request body
data = {
    "edad": 0,
    "vomit": "Ya aqui esta funcionando la vuelta"
}

# Make the POST request to the endpoint of your FastAPI app
response = requests.post("http://127.0.0.1:8000/EnviarVomito", json=data)

# Print the response
print(response.status_code)
print(response.json())
