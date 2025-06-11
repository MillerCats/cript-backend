import random
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["http://localhost:5500"] para más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Función para obtener el MCD y los coeficientes de Bezout
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

# Función para obtener el inverso modular
def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('No existe inverso modular')
    else:
        return x % m

# Genera claves RSA pequeñas
def generar_claves():
    # Primos pequeños
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)

    # e debe ser coprimo con phi
    e = 17  # Un valor común, válido aquí porque gcd(17, phi) = 1
    d = modinv(e, phi)

    return (e, n), (d, n)

# Cifra el mensaje (como una lista de números)
def cifrar(mensaje, clave_publica):
    e, n = clave_publica
    # Convertimos cada carácter a su código y lo ciframos
    return [pow(ord(c), e, n) for c in mensaje]

# Descifra el mensaje
def descifrar(cifrado, clave_privada):
    d, n = clave_privada
    # Aplicamos RSA y convertimos el número a carácter
    return ''.join([chr(pow(c, d, n)) for c in cifrado])

# Define la estructura del JSON esperado
class InputData(BaseModel):
    mensaje: str

# Endpoint que recibe un JSON y retorna otro
@app.post("/cifrar/")
async def cifrar_data(data: InputData):
    # Procesamiento: ejemplo, crear un saludo
    clave_publica, _ = generar_claves()
    cifrado = cifrar(data.mensaje, clave_publica)
    # Convertimos la lista a string legible
    texto_cifrado = ' '.join(map(str, cifrado))
    # Retornar respuesta como JSON
    return {
        "mensaje": texto_cifrado
    }

