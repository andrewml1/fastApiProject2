import json
from fastapi import FastAPI
from starlette.responses import HTMLResponse
import pruebaMAIN
from Pte import Paciente
from nlpMedico import awsMedicamentos, awsDiagnostico, constHistoria

app = FastAPI()

mds = awsMedicamentos(constHistoria.historia)
antecedente = awsDiagnostico(constHistoria.historia)

pteAPI = Paciente(35,28,75,8,7,mds,
                       antecedente,
                       False, True, 235, 2, 7,False)

@app.get("/")
def get_paciente():

    html_content = """
    <html>
        <body>
            <h1>Welcome to VEAMY!</h1>
            <p style="color: blue; font-style: italic;"> Decide who receives treatment and who does not</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/IPS/")
def get_paciente():
    # Retrieve patient information from a database or API
    # Here you can replace this with your code to retrieve patient information
    pte = pteAPI
    return {"paciente": pte.pte_tostr()}

@app.get("/home")
def get_paciente():
    return {"Estado inicial": json.loads((pteAPI.tto_tostr()))}

@app.get("/tratar")
def get_paciente():
    sPrueba=pruebaMAIN.pruebaPTE(pteAPI)
    return {"Prueba": str(sPrueba)}


@app.post("/tto")
def my_api_endpoint(request_body: dict):
    # Do something with the request body
    return {"Tratamiento recibido": request_body}


#
# class Paciente(BaseModel):
#     identif: int
#     edad: int
#     imc: float
#     tfg: int
#     hba1c: float
#     meta_hba1c: float
#     medicamento: list
#     antecedente: list
#     tolera_metform: bool
#     hipos: bool
#     hipos: str
#     glicemia: int
#     ultGlicada: int
#     ultCreatinina: int
#     tolera_aGLP1: bool
#     via: int
#     salida: bool
#     prediagnostico: str
#     tratamiento: str
#     tipoTto: str
#     subGrupoMedicamento: str
#     cuantosADO: str