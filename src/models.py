from pydantic import BaseModel
from typing import List

class Usuario(BaseModel):
    nombre: str
    public_key: tuple  # (e, n)
    private_key: tuple  # (d, n)

class Mensaje(BaseModel):
    origen: str
    destino: str
    contenido: List[int]  # mensaje cifrado

class RegistroUsuarioRequest(BaseModel):
    nombre: str

class ClavePublicaResponse(BaseModel):
    nombre: str
    public_key: tuple

class EnviarMensajeRequest(BaseModel):
    origen: str
    destino: str
    contenido: List[int]  # ya cifrado

class DescifrarRequest(BaseModel):
    cifrado: List[int]
    d: int
    n: int
