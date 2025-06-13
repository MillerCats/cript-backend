from sympy import isprime, mod_inverse
import random

def generar_primo(bits=8):
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num

def generar_claves(bits=8):
    p = generar_primo(bits)
    q = generar_primo(bits)
    while q == p:
        q = generar_primo(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while True:
        if phi % e != 0:
            break
        e += 2
    d = mod_inverse(e, phi)
    return {"public": (e, n), "private": (d, n)}

def cifrar(mensaje: str, e: int, n: int):
    return [pow(ord(c), e, n) for c in mensaje]

def descifrar(cifrado: list, d: int, n: int):
    return ''.join([chr(pow(c, d, n)) for c in cifrado])
