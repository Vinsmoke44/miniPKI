#!/usr/bin/env python3

def padding(message):
    padded_message = message + '1'
    original_length = len(message)
    padding_length = 128 - ((original_length + 1) % 128)
    padded_message += '0' * padding_length
    if original_length % 128 == 0:
        padded_message += '0' * 128
    return padded_message

def text_to_bits(text):                                         #text to binaire
    bits = ''.join(format(ord(char), '08b') for char in text)
    return bits

def bits_to_text(bits):
    text = ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))
    return text

def segment(bits):
    #divise en blocs de 128 bits
    blocks = [bits[i:i+128] for i in range(0, len(bits), 128)]
    # Applique le bourrage à la fin de la dernière partie si nécessaire
    last_block_index = len(blocks) - 1
    blocks[last_block_index] = padding(blocks[last_block_index])
    return blocks


def permutation_initiale(message):
    B = segment(text_to_bits(message))
    print("Blocs avant permutation initia:", B)

    # Applique la permutation initiale à chaque bloc
    resultat = [''.join(bloc[(32 * i) % 127] for i in range(128)) for bloc in B]
    print("Blocs après permutation initia:", resultat)
    # Concatène les blocs pour obtenir le message chiffré final
    # permutI = ''.join(resultat)
    return resultat


def permutation_finale(bits):
    # B = segment(bits)
    print("Blocs avant permutation finale:", bits)

    # Inverse la permutation initiale à chaque bloc
    resultat = [''.join(bloc[(4 * i) % 127] for i in range(128)) for bloc in bits]
    print("Blocs après permutation finale:", resultat)
    # Concatène les blocs pour obtenir le message déchiffré final
    permutF = (resultat)
    return permutF



M=input("Entrez ce que vous souhaitez chiffrer :")

permute = permutation_initiale(M)

permF = ''.join(permutation_finale(permute))

print((bits_to_text(permF)))
# msg = bits_to_text(permF)
# print(msg)

