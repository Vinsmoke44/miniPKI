#!/usr/bin/env python3

def padding(message):
    original_length = len(message)
    if len(message) % 128 == 0:
        padded_message = message
    else:
        padded_message = message + '1'
        padding_length = 128 - ((original_length + 1) % 128)
        padded_message += '0' * padding_length
    return padded_message

def text_to_bits(text):                                         #text to binaire
    bits = ''.join(format(ord(char), '08b') for char in text)
    return bits

def bits_to_text(bits):
    text = ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))
    return text

# def segment(bits):
#     #divise en blocs de 128 bits
#     blocks = [bits[i:i+128] for i in range(0, len(bits), 128)]
#     # Applique le bourrage à la fin de la dernière partie si nécessaire
#     last_block_index = len(blocks) - 1
#     blocks[last_block_index] = padding(blocks[last_block_index])
#     return blocks


def permutation_initiale(bloc):
    result = 0
    for i in range(128):
        # Obtient la valeur du bit situé à (32 * i) % 127
        bit = (bloc >> ((32 * i) % 127)) & 1

        # Place la valeur du bit à la position i
        result |= bit << i
    return result


def permutation_finale(bloc):
    result = 0
    for i in range(128):
        # Obtient la valeur du bit à la position 
        bit = (int(bloc, 2) >> ((4 * i) % 127)) & 1
        # Place la valeur du bit à la position i dans le nouveau bloc
        result |= bit << i
    return result

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

def left_gap(value, shift, bit_length=32):
    # Assurez-vous que la valeur est représentée sur le nombre de bits spécifié
    value = value & ((1 << bit_length) - 1)
    # Effectuez la rotation vers la gauche
    result = (value << shift)
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

def calculate_sboxes():
    sbox_0 = [
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
    
    sboxes = []
    sboxes.append(sbox_0)

    for k in range(1, 32):
        new_sbox = [row[:] for row in sboxes[k-1]]  # Deep copy of sboxes[k-1]
        for index_box in range(32):
            for index_bits in range(16):
                i = index_bits + new_sbox[index_box][index_bits]
                j = new_sbox[i][index_bits]
                # Swap
                new_sbox[index_box][index_bits], new_sbox[index_box][j] = new_sbox[index_box][j], new_sbox[index_box][index_bits]
        sboxes.append(new_sbox)
    return sboxes


def apply_sbox(input_nibble, sbox, row):
    # Assurez-vous que l'entrée est un entier de 4 bits
    col = input_nibble & 0xF
    
    # Récupérez la valeur de la S-box
    output_nibble = sbox[row][col]
    
    return output_nibble

def B_iterations(B_0, K_i):
    for j in range(31):
        sbox = j #recupere sboxes[j]
        res_xor = segment_bits(xor(B_0, K_i[j]), 4)
        appli_sbox = []
        for i in range(32):
            appli_sbox.append(format(apply_sbox(int(res_xor[i]), sboxes[j], i), '04b'))
        X0, X1, X2, X3 = segment_bits(''.join(appli_sbox), 32)
        X0 = format(rotate_left(int(X0, 2), 3, 32), '032b')
        X2 = format(rotate_left(int(X2, 2), 3, 32), '032b')
        X1 = xor(xor(X1, X0), X2)
        X3 = xor(xor(X3, X2), format(left_gap(int(X0, 2), 3), '032b'))
        X1 = format(rotate_left(int(X1, 2), 1, 32), '032b')
        X3 = format(rotate_left(int(X3, 2), 7, 32), '032b')
        X0 = xor(xor(X0, X1), X3)
        X2 = xor(xor(X2, X3), format(left_gap(int(X1, 2), 7), '032b'))
        X0 = format(rotate_left(int(X0, 2), 5, 32), '032b')
        X2 = format(rotate_left(int(X2, 2), 2, 32), '032b')
        B_0 = ''.join([X0, X1, X2, X3])
    res_xor = segment_bits(xor(B_0, K_i[31]), 4)
    appli_sbox = []
    for i in range(32):
        appli_sbox.append(format(apply_sbox(int(res_xor[i]), sboxes[31], i), '04b'))
    B_32 = xor(''.join(appli_sbox), K_i[32])
    return B_32

sboxes = calculate_sboxes()

message = ('hello world hehe')
M = segment_bits(padding(text_to_bits(message)), 128)
# for i in range(len(M)):
print("bas:", format(int(M[0], 2), '0128b'))
B_0 = format(permutation_initiale(int(M[0], 2)), '0128b')
print("B_0:", B_0)
test = permutation_finale(B_0)
print("fin:", format(test, '0128b'))


# K = "1111111111111010111111111011111111111100001111111111110111101111111111111111101111111111111110111111111111111111110001111111111111001111111111111111111111111101111111111100011111111111111111111111111111111111011111111111111111111111101111111111111111111110"
# K_i = K_i_gen(K)

# B_32 = B_iterations(B_0, K_i)

# print("B_32", B_32)
# print(sboxes[1])
# C = format(permutation_finale(B_32), '0128b')
# print("C:", C)


# permF = ''.join(permutation_finale(permute))
# print((bits_to_text(permF)))
# msg = bits_to_text(permF)
# print(msg)