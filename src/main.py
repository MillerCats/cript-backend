from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rsa_utils import generar_claves, cifrar, descifrar

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["http://localhost:5500"] para más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Claves globales simuladas por sesión
claves = generar_claves(bits=8)

class CifrarRequest(BaseModel):
    mensaje: str
    e: int
    n: int

class DescifrarRequest(BaseModel):
    cifrado: list
    d: int
    n: int

@app.get("/clave")
def obtener_clave_publica():
    e, n = claves["public"]
    d, _ = claves["private"]
    return {"e": e, "n": n, "d": d}

@app.post("/cifrar")
def cifrar_mensaje(req: CifrarRequest):
    return {"cifrado": cifrar(req.mensaje, req.e, req.n)}

@app.post("/descifrar")
def descifrar_mensaje(req: DescifrarRequest):
    return {"mensaje": descifrar(req.cifrado, req.d, req.n)}
