from fastapi import FastAPI
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
##App
app = FastAPI()


class Student(BaseModel):
    edad: int
    imc: float
    tfg: float
    hba1c: float
    meta_hba1c = int
    medicamento: str
    antecedente: str
    tolera_metform: bool
    hipos: bool
    glicemia: float
    ultGlicada: int
    ultCreatinina: int
    tolera_aGLP1: bool

from pydantic import BaseModel

class UserData(BaseModel):
    def __init__(self, name: str, email: str, password: str):
        self.name = 'Prueba'
        self.email = 'Correo'
        self.password = 'password'

@app.get("/user")
def create_user(user: UserData):
    return {"name": user.name, "email": user.email, "password": user.password}


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/hello/veamy")
def say_hello():
    return {"message": f"Welcome to Veamy",
            "Data":"1,2,3,4"}

@app.get("/get-paciente/{paciente_id}")
def get_paciente(paciente_id:int):
    return Pacientes[paciente_id]


class Paciente(BaseModel):
  name: str
  email: str
  password: str

##Base de datos Mongo para almacenar lo que se envia
Pacientes={
    1:{
        'name' : "Carlos",
        'email' : 'email@carlos',
        'password' : 'carlinhos'
    }
}

@app.post("/Enviar")
def envio_info(numPte:int, pte:Paciente):
        if numPte in Pacientes:
            return {"Error":"Paciente ya existe"}
        else:
            Pacientes[numPte]=pte
            return Pacientes[numPte]






