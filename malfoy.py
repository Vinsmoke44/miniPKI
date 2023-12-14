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
    # print("Blocs avant permutation initia:", B)

    # Applique la permutation initiale à chaque bloc
    resultat = [''.join(bloc[(32 * i) % 127] for i in range(128)) for bloc in B]
    # print("Blocs après permutation initia:", resultat)
    # Concatène les blocs pour obtenir le message chiffré final
    # permutI = ''.join(resultat)
    return resultat


def permutation_finale(bits):
    # B = segment(bits)
    # print("Blocs avant permutation finale:", bits)

    # Inverse la permutation initiale à chaque bloc
    resultat = [''.join(bloc[(4 * i) % 127] for i in range(128)) for bloc in bits]
    # print("Blocs après permutation finale:", resultat)
    # Concatène les blocs pour obtenir le message déchiffré final
    permutF = (resultat)
    return permutF

def segment_bits(K, j):
    blocks = [K[i:i+j] for i in range(0, len(K), j)]
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
    w = segment_bits(K, 32)
    w_i = w.copy()
    K_i = [''.join((w[0], w[1], w[2], w[3]))]
    

    for i in range(8, 132):
        w.append(xor(xor(xor(xor(xor(w[i-8], w[i-5]), w[i-3]), w[i-1]), constante), bin(i)[2:]))
        rotated_value = rotate_left(int(w[i], 2), 11, 32)
        w_i.append(format(rotated_value, '032b'))
    
    for i in range (1,33):
        K_i.append(''.join((w[i*4], w[i*4+1], w[i*4+2], w[i*4+3])))
    return K_i

def permute_sboxes(sbox):
    new_sbox = [row[:] for row in sbox]  # Crée une copie de la S-box d'origine
    # new_sbox = sbox.copy()
    for index_box in range(32):
        for index_bits in range(16):
            i = (index_bits + sbox[index_box][index_bits]) % 32
            j = sbox[i][index_bits]
            # Swap
            new_sbox[index_box][index_bits], new_sbox[index_box][j] = new_sbox[index_box][j], new_sbox[index_box][index_bits]

    return new_sbox

def calculate_sboxes():
    sbox = [
[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
[4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

    sboxes = [sbox]  # Initialise la liste avec la S-box d'origine

    for _ in range(1, 32):
        sbox = permute_sboxes(sbox)
        sboxes.append(sbox)

    return sboxes


def apply_sbox(input_nibble, sbox, row):
    # Assurez-vous que l'entrée est un entier de 4 bits
    col = input_nibble & 0xF
    
    # Récupérez la valeur de la S-box
    output_nibble = sbox[row][col]
    
    return output_nibble

# def linear_transfo(B_0, K_i, sboxes):
#     B_i = [B_0]
#     print(xor(''.join(B_i[0]), K_i[0]))
#     print(permute_sboxes((xor(''.join(B_i[0]), K_i[0]))))
    
#     for i in range(33):
#         xor = (xor(''.join(B_i[i]), K_i[i]))
#         print((sboxes[i])(xor(''.join(B_i[i]), K_i[i])))
#         print(X1)

sboxes = calculate_sboxes()

message = input("Entrez ce que vous souhaitez chiffrer :")
B_0 = permutation_initiale(message)
B_i = [B_0]

K = "0101111010100110111001111001111101010011111000001010110001100011110011000010101101111001111010111110110111110011101110110100111001111111011110101100000011110011011011100000110101010100001101100111001010011011000000100000011011011000100100110001001101010010"
K_i=K_i_gen(K)


res_xor = segment_bits(xor(''.join(B_0), K_i[0]), 4)
appli_sbox = []
# for j in range(32):
#     sbox = j #recupere sboxes[j]
for i in range(32):
    appli_sbox.append(format(apply_sbox(int(res_xor[i]), sboxes[0], i), '04b'))
X0, X1, X2, X3 = segment_bits(''.join(appli_sbox), 32)
print(X3)


# permF = ''.join(permutation_finale(permute))
# print((bits_to_text(permF)))
# msg = bits_to_text(permF)
# print(msg)