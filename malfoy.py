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

def segment_clef(K):
    print("La clé secrète est:", K)
    blocks = [K[i:i+32] for i in range(0, len(K), 32)]
    return blocks

def xor(x, y):
    return '{1:0{0}b}'.format(len(x), int(x, 2) ^ int(y, 2))

def rotate_left(value, shift, bit_length=32):
    # Assurez-vous que la valeur est représentée sur le nombre de bits spécifié
    value = value & ((1 << bit_length) - 1)
    # Effectuez la rotation vers la gauche
    result = (value << shift) | (value >> (bit_length - shift))
    return result & ((1 << bit_length) - 1)

def K_i_gen(K):
    constante = '10011110001101110111100110111001' #constante omega from hex to binary
    w = segment_clef(K)
    w_i = w.copy()
    K_i = [''.join((w[0], w[1], w[2], w[3]))]
    

    for i in range(8, 132):
        w.append(xor(xor(xor(xor(xor(w[i-8], w[i-5]), w[i-3]), w[i-1]), constante), bin(i)[2:]))
        rotated_value = rotate_left(int(w[i], 2), 11, 32)
        w_i.append(format(rotated_value, '032b'))
    
    for i in range (1,33):
        K_i.append(''.join((w[i*4], w[i*4+1], w[i*4+2], w[i*4+3])))
    return K_i

# M=input("Entrez ce que vous souhaitez chiffrer :")
# permute = permutation_initiale(M)
# permF = ''.join(permutation_finale(permute))
# print((bits_to_text(permF)))
# msg = bits_to_text(permF)
# print(msg)

K = "0101111010100110111001111001111101010011111000001010110001100011110011000010101101111001111010111110110111110011101110110100111001111111011110101100000011110011011011100000110101010100001101100111001010011011000000100000011011011000100100110001001101010010"
w=K_i_gen(K)
print(w)