from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.tables import User
from src.models import UserCreate, UserLogin

def registrar_usuario(db: Session, usuario: UserCreate):
    if db.query(User).filter(User.correo == usuario.correo).first():
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    nuevo_usuario = User(
        nombre=usuario.nombre,
        correo=usuario.correo,
        user_pass=usuario.user_pass
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"process": True, "user_id": nuevo_usuario.id}

def iniciar_sesion(db: Session, login_data: UserLogin):
    usuario = db.query(User).filter(User.nombre == login_data.nombre).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.user_pass != login_data.user_pass:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    return {"process": True, "user_id": usuario.id}
