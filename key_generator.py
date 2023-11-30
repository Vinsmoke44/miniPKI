import random

def est_premier(nombre, iterations=5):
    if nombre < 2:
        return False
    for _ in range(iterations):
        a = random.randint(2, nombre - 2)
        if pow(a, nombre - 1, nombre) != 1:
            return False
    return True

def generer_nombre_premier(bits):
    nombre = random.getrandbits(bits)
    while not est_premier(nombre):
        nombre = random.getrandbits(bits)
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
    e = 65537  # Généralement choisi comme 2^16 + 1 pour des raisons de performance

    # Calcul de l'exposant privé d
    d = inverse_modulaire(e, phi_n)

    # Clé publique
    cle_publique = (n, e)

    # Clé privée
    cle_privee = (n, d)

    return cle_publique, cle_privee

# Générer une paire de clés de 1024 bits
cle_publique, cle_privee = generer_cles(256) 

print("Clé publique (n, e) :", cle_publique)
print("Clé privée (n, d) :", cle_privee)
