from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    clave_publica = Column(String(4096), nullable=False)

    # Relaciones
    mensajes_enviados = relationship("Message", foreign_keys="Message.remitente_id", backref="remitente")
    mensajes_recibidos = relationship("Message", foreign_keys="Message.destinatario_id", backref="destinatario")

class Message(Base):
    __tablename__ = 'mensajes'
    
    id = Column(Integer, primary_key=True)
    remitente_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    destinatario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    asunto = Column(String(200))
    mensaje_cifrado = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow, nullable=False)
    leido = Column(Boolean, default=False)

    # Las relaciones están definidas en la clase User
