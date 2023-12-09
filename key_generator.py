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

def generate_asymetrical(bits):
    p = generer_nombre_premier(bits)
    q = generer_nombre_premier(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Choix d'un exposant public e
    e = 65537 

    # Calcul de l'exposant privé d
    d = inverse_modulaire(e, phi_n)

    # Clé publique
    # cle_publique = (n, e)

    # # Clé privée
    # cle_privee = (n, d)

    return n, e , d

def generate_serpent_key():
    # La longueur de la clé en bits
    key_length_bits = 256
    serpent_key_bits = [random.choice([0, 1]) for _ in range(key_length_bits)]
    serpent_key = "".join(map(str, serpent_key_bits))
    return serpent_key


def encrypt_rsa(plaintext, n, e):
    ciphertext = pow(plaintext, e, n)
    return ciphertext

def decrypt_rsa(ciphertext, n , d):
    plaintext = pow(ciphertext, d, n)
    return plaintext

# Test generer asymetrique et symetrique
# cle_publique, cle_privee = generate_asymetrical(512)
# cle_symetrique = generate_serpent_key()

# Test chiffrer clé symetrique avec clé publique 
# print(cle_symetrique)
# cle_symetrique_int = int("".join(map(str, cle_symetrique)), 2)
# cle_symetrique_chiffree = encrypt_rsa(cle_symetrique_int, cle_publique)
# print("Clé symétrique chiffrée :", cle_symetrique_chiffree)
 
# Test dechiffrer clé symetrique avec clés privée
#cle_symetrique_dechiffree = decrypt_rsa(cle_symetrique_chiffree, cle_privee)
# cle_symetrique_dechiffree_bits = [int(b) for b in bin(cle_symetrique_dechiffree)[2:].zfill(128)]
# serpent_key_decrypt = "".join(map(str, cle_symetrique_dechiffree_bits))
# print("Clé symétrique déchiffrée en bits :", serpent_key_decrypt)


#Test clé asymetrique
# cle_publique, cle_privee = generate_asymetrical(512) 
# print("Clé publique (n, e) :", cle_publique)
# print("Clé privée (n, d) :", cle_privee)

# Test clé symetrique :
# serpent_key_bits = generate_serpent_key()
# print("Clé Serpent générée en bits:", serpent_key_bits)
