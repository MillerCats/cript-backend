from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserLogin
from jose import jwt
import json
import base64
import hashlib

def firmar_jwt() -> str: 
    """
    Crea un JWT personalizado y lo firma manualmente con la clave privada RSA.
    """
    def base64url_encode(data: bytes):
        return base64.urlsafe_b64encode(data).rstrip(b'=')

    header = {"alg": "RS256", "typ": "JWT"}
    header_json = json.dumps(header, separators=(',', ':')).encode()
    payload_json = json.dumps(payload, separators=(',', ':')).encode()

    header_b64 = base64url_encode(header_json)
    payload_b64 = base64url_encode(payload_json)

    mensaje = header_b64 + b'.' + payload_b64

    # Hash SHA-256 del mensaje (como "pre-firma")
    hash_mensaje = int.from_bytes(hashlib.sha256(mensaje).digest(), byteorder='big')

    # Firma RSA manual: signature = hash^d mod n
    firma = pow(hash_mensaje, d, n)
    firma_bytes = firma.to_bytes((firma.bit_length() + 7) // 8, byteorder='big')
    firma_b64 = base64url_encode(firma_bytes)

    return (mensaje + b'.' + firma_b64).decode()


def registrar_usuario(db: Session, usuario: UserCreate):
    if db.query(User).filter(User.correo == usuario.correo).first():
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    nuevo_usuario = User(
        nombre=usuario.nombre,
        correo=usuario.correo,
        clave_publica=usuario.clave_publica
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def iniciar_sesion(db: Session, login_data: UserLogin):
    usuario = db.query(User).filter(User.correo == login_data.correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.clave_publica != login_data.clave_publica:
        raise HTTPException(status_code=401, detail="Clave pública incorrecta")

    return usuario
