from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, Query
from typing import List, Dict, Optional, Any
from fastapi.middleware.cors import CORSMiddleware
from src.models import *
from sqlalchemy.orm import Session
import json
from src.auth import registrar_usuario, iniciar_sesion
from src.database import init_db, get_db

app = FastAPI()

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["http://localhost:5500"] para más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para registrar
@app.post("/registro")
def registrar(user: UserCreate, db: Session = Depends(get_db)):
    return registrar_usuario(db, user)

# Endpoint para login
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return iniciar_sesion(db, user)

class ConnectionManager:
    def __init__(self):
        self.authenticated_users: Dict[str, Dict[str, Any]] = {} # id -> {"conn": websocket, "nombre": str}
        self.guests: List[WebSocket] = []  # solo ven
        self.messages: List[str] = []  # historial de mensajes en texto plano
        self.public_keys: Dict[str, Dict[str, int]] = {}  # id -> {"e": ..., "n": ...}

    def save_public_key(self, user_id: str, public_key: Dict[str, int]):
        self.public_keys[user_id] = public_key

    def get_public_key(self, user_id: str):
        return self.public_keys.get(user_id)
    
    async def connect(self, websocket: WebSocket, user_id: Optional[str], user_name: Optional[str]):
        await websocket.accept()
        if user_id:
            self.authenticated_users[user_id] = {
            "conn": websocket,
            "nombre": user_name
            }
            await self.notify_user_list()  # 👈 Notifica cambio
        else:
            self.guests.append(websocket)
            # enviar historial a visitantes
            for msg in self.messages:
                await websocket.send_text(msg)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.guests:
            self.guests.remove(websocket)
        else:
            for uid, data in list(self.authenticated_users.items()):
                if data["conn"] == websocket:
                    del self.authenticated_users[uid]
        await self.notify_user_list() # 👈 Notifica cambio

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.authenticated_users:
            await self.authenticated_users[user_id]["conn"].send_text(message)

    async def broadcast(self, message: str, sender_id: str):
        self.messages.append(message)  # guardar mensaje

        # enviar a todos los autenticados excepto al remitente
        for uid, data in self.authenticated_users.items():
            if uid != sender_id:
                await data["conn"].send_text(message)

        # enviar a todos los visitantes
        for guest in self.guests:
            await guest.send_text(message)
    
    def get_connected_users(self, exclude_user_id: Optional[str] = None):
        result = []
        for uid, data in self.authenticated_users.items():
            if uid == exclude_user_id:
                continue
            result.append({
                "id": uid,
                "nombre": data["nombre"]
            })
        return result
    
    async def notify_user_list(self):
        for uid, data in self.authenticated_users.items():
            conn = data["conn"]  # 👈 Aquí sí es un WebSocket
            conectados = self.get_connected_users(exclude_user_id=uid)
            mensaje = json.dumps({
                "tipo": "usuarios_conectados",
                "conectados": conectados
            })
            await conn.send_text(mensaje)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, user_id: Optional[str] = Query(None), user_name: Optional[str] = Query(None)):
    await manager.connect(websocket, user_id, user_name)

    try:
        while True:
            data = await websocket.receive_text()
            if user_id:
                try:
                    parsed = json.loads(data)

                    if parsed.get("tipo") == "public_key":
                        manager.save_public_key(user_id, parsed["publicKey"])
                        continue

                    receiver_id = str(parsed.get("to"))
                    text = parsed.get("text")

                    if receiver_id and text:
                        message_json = json.dumps({
                            "from": user_id,
                            "text": text,
                            "public_key": manager.get_public_key(receiver_id)
                        })
                        manager.messages.append(message_json)
                        await manager.send_personal_message(message_json, receiver_id)
                        for guest in manager.guests:
                            await guest.send_text(message_json)
                    else:
                        await websocket.send_text("Faltan datos: 'to' o 'text'.")
                except json.JSONDecodeError:
                    await websocket.send_text("Formato JSON inválido.")
            else:
                await websocket.send_text("No tienes permiso para enviar mensajes.")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

@app.get("/usuarios/conectados")
def usuarios_conectados(current_user: Optional[str] = Query(None)):
    return {"conectados": manager.get_connected_users(exclude_user_id=current_user)}

@app.get("/usuarios/{user_id}/clave-publica")
def obtener_clave_publica(user_id: str):
    clave = manager.get_public_key(user_id)
    if not clave:
        return {"error": "Clave no encontrada"}
    return clave
