import random
import math
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

def factorizar_n(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i, n // i
    raise ValueError("No se pudo factorizar n.")

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

# Descifrar el mensaje cifrado sin conocer d (vulnerando RSA)
def vulnerar_rsa(clave_publica, cifrado):
    e, n = clave_publica
    print(f"[+] Intentando vulnerar n = {n}...")

    p, q = factorizar_n(n)
    print(f"[+] Éxito: n = p * q = {p} * {q}")

    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    print(f"[+] Calculado d = {d}")

    # Descifrar
    descifrado = ''.join([chr(pow(c, d, n)) for c in cifrado])
    return descifrado

if __name__ == "__main__":
    mensaje = input("Ingresa una palabra: ")
    clave_publica, clave_privada = generar_claves()
    print(f"Clave pública: {clave_publica}")
    print(f"Clave privada: {clave_privada}")

    cifrado = cifrar(mensaje, clave_publica)
    print(f"Mensaje cifrado: {cifrado}")
    # Supón que este es el mensaje cifrado interceptado
    mensaje_descifrado = vulnerar_rsa(clave_publica, cifrado)
    print(f"🔓 Mensaje descifrado (vulnerado): {mensaje_descifrado}")

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

