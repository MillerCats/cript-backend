from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from src.rsa_utils import generar_claves, cifrar, descifrar

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

# --- WebSocket: Comunicación entre usuarios ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)