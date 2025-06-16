import random
import math

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


def factorizar_n(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i, n // i
    raise ValueError("No se pudo factorizar n.")

# Descifrar el mensaje cifrado sin conocer d (vulnerando RSA)
def vulnerar_rsa(clave_publica):
    e, n = clave_publica
    print(f"[+] Intentando vulnerar n = {n}...")

    p, q = factorizar_n(n)
    print(f"[+] Éxito: n = p * q = {p} * {q}")

    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    print(f"[+] Calculado d = {d}")

    return (d, n)

def corroborar_clave_privada(clave_privada, clave_publica):
    return vulnerar_rsa(clave_publica) == clave_privada


if __name__ == "__main__":
    print("Calcularesmos el valor de d en la clave privada")
    e = int(input("Ingresa e: "))
    n = int(input("Ingresa n: "))
    clave_publica = (e, n)
    print(f"Clave pública: {clave_publica}")

    # Supón que este es el mensaje cifrado interceptado
    clave_privada = vulnerar_rsa(clave_publica)
    print(f"🔓 Clave privada (vulnerado): {clave_privada}")
