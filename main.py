from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from src.rsa_utils import generar_claves, cifrar, descifrar
from src.models import *
from src.vulnerar_util import corroborar_clave_privada
from sqlalchemy.orm import Session
from database import db_session, init_db
from schemas import UserCreate, UserLogin, UserResponse
from auth import registrar_usuario, iniciar_sesion

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["http://localhost:5500"] para más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar DB al arrancar
@app.on_event("startup")
def on_startup():
    init_db()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()

# Endpoint para registrar
@app.post("/registro", response_model=UserResponse)
def registrar(user: UserCreate, db: Session = Depends(get_db)):
    return registrar_usuario(db, user)

# Endpoint para login
@app.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return iniciar_sesion(db, user)