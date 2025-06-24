from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    user_pass = Column(String(100), nullable=False)