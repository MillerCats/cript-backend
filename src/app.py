import random

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

# Ejemplo de uso
if __name__ == "__main__":
    mensaje = input("Ingresa una palabra corta para cifrar: ")

    clave_publica, clave_privada = generar_claves()
    print(f"Clave pública: {clave_publica}")
    print(f"Clave privada: {clave_privada}")

    cifrado = cifrar(mensaje, clave_publica)
    print(f"Mensaje cifrado: {cifrado}")

    descifrado = descifrar(cifrado, clave_privada)
    print(f"Mensaje descifrado: {descifrado}")
