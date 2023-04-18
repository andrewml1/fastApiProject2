from fastapi import FastAPI
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
from pymongo import MongoClient
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

##App
app = FastAPI()




@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/get-paciente/{paciente_id}")
def get_paciente(paciente_id:int):
    return Pacientes[paciente_id]

# class Paciente(BaseModel):
#   name: str
#   email: str
#   password: str

##Base de datos Mongo para almacenar lo que se envia
Pacientes={
    1:{
        'name' : "Carlos",
        'email' : 'email@carlos',
        'password' : 'carlinhos'
    }
}

uri = "mongodb+srv://andrewml1:ludacris@cluster0.iwdoxtk.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
##Test el cliente
db = client.test
##Crear objeto collection (sobre este es que va a insertar los datos)
collection = db.my_collection


class Paciente(BaseModel):
    edad: int
    imc: float
    tfg: float
    hba1c: float
    meta_hba1c: int
    medicamento: str
    antecedente: str
    tolera_metform: bool
    hipos: bool
    glicemia: float
    ultGlicada: int
    ultCreatinina: int
    tolera_aGLP1: bool

@app.post("/Enviar")
def envio_info(numPte:int, pte:Paciente):
        if numPte in Pacientes:
            return {"Error":"Paciente ya existe"}
        else:
            document = {
            "numPte": numPte,
            "edad": pte.edad,
            "imc": pte.imc,
            "tfg": pte.tfg,
            "hba1c": pte.hba1c,
            "meta_hba1c": pte.meta_hba1c,
            "medicamento": pte.medicamento,
            "antecedente": pte.antecedente,
            "tolera_metform": pte.tolera_metform,
            "hipos": pte.hipos,
            "glicemia": pte.glicemia,
            "ultGlicada": pte.ultGlicada,
            "ultCreatinina": pte.ultCreatinina,
            "tolera_aGLP1": pte.tolera_aGLP1}

        result = collection.insert_one(document)

            # Pacientes[numPte]=pte
            # return Pacientes[numPte]
        return {"message": "registro agregada(o)"}







