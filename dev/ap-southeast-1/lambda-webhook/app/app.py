from typing import Union
from fastapi import FastAPI
from mangum import Mangum
from fastapi.responses import JSONResponse

app = FastAPI()
handler = Mangum(app)

@app.get("/")
def read_root():
    return {"Welcome to": "My first FastAPI deployment using Docker image"}

@app.get("/{text}")
def read_item(text: str):
    return JSONResponse({"result": text})
