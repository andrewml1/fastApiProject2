from fastapi import FastAPI

##App
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/veamy")
async def say_hello():
    return {"message": f"Welcome to Veamy",
            "Data":"1,2,3,4"}



@app.get("/hello/pedacito")
async def hola_pedacito():
    return {"message": f"Hola Pedacito, estamos aqui en etapa de pruebas y todo esta saliendo bien",
            "Fecha":"06/04/23"}


