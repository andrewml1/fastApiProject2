from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/veamy")
async def say_hello():
    return {"message": f"Welcome to Veamy",
            "Data":"1,2,3,4"}
