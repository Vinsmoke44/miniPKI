import random

def is_prime(nombre, iterations=5):
    for _ in range(iterations):
        a = random.randint(2, nombre - 2)
        if pow(a, nombre - 1, nombre) != 1:
            return False
    return True

def generer_nombre_premier(bits):
    inf = 2**bits
    sup = int(1.2 * 2**bits)   
    nombre = random.randint(inf, sup)   
    while not is_prime(nombre):
        nombre = random.randint(inf, sup)   
    return nombre

def pgcd(a, b):
    while b:
        a, b = b, a % b
    return a

def inverse_modulaire(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generer_cles(bits):
    p = generer_nombre_premier(bits)
    q = generer_nombre_premier(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Choix d'un exposant public e
    e = 65537 

    # Calcul de l'exposant privé d
    d = inverse_modulaire(e, phi_n)

    # Clé publique
    cle_publique = (n, e)

    # Clé privée
    cle_privee = (n, d)

    return cle_publique, cle_privee

cle_publique, cle_privee = generer_cles(512) 

print("Clé publique (n, e) :", cle_publique)
print("Clé privée (n, d) :", cle_privee)
