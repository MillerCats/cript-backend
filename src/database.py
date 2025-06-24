from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# Datos de conexión (modifica según tu entorno)
SERVER = 'localhost'  # o IP del servidor SQL
DATABASE = 'rsaDB'
USERNAME = 'sa'
PASSWORD = '1234'

# Cadena de conexión usando pyodbc
DATABASE_URL = (
    f"mssql+pytds://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}"
)

engine = create_engine(DATABASE_URL, echo=True, future=True)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

def init_db():
    from src.tables import User  # Importa modelos aquí para registrar las tablas
    Base.metadata.create_all(bind=engine)

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()