from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Define la estructura del JSON esperado
class InputData(BaseModel):
    mensaje: str

# Endpoint que recibe un JSON y retorna otro
@app.post("/cifrar/")
async def cifrar_data(data: InputData):
    # Procesamiento: ejemplo, crear un saludo
    saludo = f"Hola {data.nombre}, tienes {data.edad} años."

    # Retornar respuesta como JSON
    return {
        "mensaje": saludo
    }
