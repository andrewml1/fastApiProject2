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


##Base de datos Mongo para almacenar lo que se envia
Pacientes={
    1:{
        'name' : "Carlos",
        'email' : 'email@carlos',
        'password' : 'carlinhos'
    }
}

##Mongo DB conexion:
uri = "mongodb+srv://andrewml1:ludacris@cluster0.iwdoxtk.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.test
##Crear objeto collection (sobre este es que va a insertar los datos)
collection = db.my_collection

##Clase paciente con valores por defecto
class Paciente(BaseModel):
    edad: int = 0
    imc: float = 20.0
    tfg: float = 70.0
    hba1c: float = 7.0
    meta_hba1c: int = 7
    medicamento: str = "Incluir medicamentos"
    antecedente: str = "Incluir antecedentes"
    tolera_metform: bool = True
    hipos: bool = False
    glicemia: float = 140.0
    ultGlicada: int = 2
    ultCreatinina: int = 3
    tolera_aGLP1: bool = True

@app.post("/Enviar")
def envio_info(numPte:int, pte:Paciente):
        if any(value is None for value in pte.dict().values()):  # Verifica que todos los valores del objeto Paciente se han completado
            return {"Error": "Debe completar todos los campos requeridos."}
        else:
            document = {"edad": pte.edad,
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

        ##Insercion en la BDs
        result = collection.insert_one(document)

        return {"message": "registro agregada(o)"}







