#!/usr/bin/env python3

def text_to_bits(text):
    # First thing to do, switch the message we want to send from ascii to binary
    bits = ''.join(format(ord(char), '08b') for char in text)
    return bits

def padding(message):
    
    original_length = len(message)
    if len(message) % 128 == 0:
        # If message=128, we don't add anything to the original message
        padded_message = message
    else:
        # Else, we add a 1 followed by 0s until it's a 128 multiple
        padded_message = message + '1'
        padding_length = 128 - ((original_length + 1) % 128)
        padded_message += '0' * padding_length
    return padded_message

def permutation_initiale(IPTable, bloc):
    if len(bloc) != len(IPTable):
        # The permuted bloc has the same len as the permutation table
        raise ValueError
    result = ""
    for i in range(len(IPTable)):
        # We use the initial permutation table to permute the bloc
        result = result + bloc[IPTable[i]]
    return result

def permutation_finale(FPTable, bloc):
    if len(bloc) != len(FPTable):
        # The permuted bloc has the same len as the permutation table
        raise ValueError
    result = ""
    for i in range(len(FPTable)):
        # We use the final permutation table to permute the bloc
        result = result + bloc[FPTable[i]]
    return result

def segment_bits(K, j):
    # Takes a K bloc and segment it in j-bits blocs
    blocks = [K[i:i+j] for i in range(0, len(K), j)]
    return blocks

def xor(x, y):
    # Xor function between x and y
    return '{1:0{0}b}'.format(len(x), int(x, 2) ^ int(y, 2))

def rotate_left(value, shift, bit_length=32):
    # We first make sure that value=bit_length
    value = value & ((1 << bit_length) - 1)
    # Left rotation without losing any bits
    result = (value << shift) | (value >> (bit_length - shift))
    return result & ((1 << bit_length) - 1)

def left_gap(value, shift, bit_length=32):
    # We first make sure that value=bit_length
    value = value & ((1 << bit_length) - 1)
    # Left gap, loss of the first $shift bits
    result = (value << shift)
    return result & ((1 << bit_length) - 1)

def K_i_gen(K):
    # Omega constant from hex to binary
    constant = '10011110001101110111100110111001'
    # K segmentation to get the first 8 w blocs
    w = segment_bits(K, 32)
    w_i = w.copy()
    # K_i initialisation with K_i[0]
    K_i = [''.join((w[0], w[1], w[2], w[3]))]
    

    for i in range(8, 132):
        # Formation of the additional w blocs 
        w.append(xor(xor(xor(xor(xor(w[i-8], w[i-5]), w[i-3]), w[i-1]), constant), bin(i)[2:]))
        rotated_value = rotate_left(int(w[i], 2), 11, 32)
        w_i.append(format(rotated_value, '032b'))
    
    for i in range (1,33):
        # K_i completion thanks to the w blocs
        K_i.append(''.join((w[i*4], w[i*4+1], w[i*4+2], w[i*4+3])))
    return K_i

def calculate_sboxes():
    # S0 built following DES 32 tables for initialization
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
        # Deep copy of sboxes[k-1]
        new_sbox = [row[:] for row in sboxes[k-1]]
        # Then, we find sbox[i] with permutations on sbox[i-1]
        for index_box in range(32):
            for index_bits in range(16):
                i = index_bits + new_sbox[index_box][index_bits]
                j = new_sbox[i][index_bits]
                # We swap attributes in the sbox
                new_sbox[index_box][index_bits], new_sbox[index_box][j] = new_sbox[index_box][j], new_sbox[index_box][index_bits]
        sboxes.append(new_sbox)
    return sboxes


def apply_sbox(input_nibble, sbox, row):
    # The 4-bits nibble forms the column of the sbox
    col = input_nibble
    # We find the output value at the correct location
    output_nibble = sbox[row][col]
    return output_nibble

def B_iterations(B, K_i):
    sboxes = calculate_sboxes()
    # The input is B_0 and K_i table and the ouput will be B_32
    for j in range(31):
        # After we xored B with K_i, we segment the result in 4-bits blocs
        res_xor = segment_bits(xor(B, K_i[j]), 4)
        appli_sbox = []
        for i in range(32):
            # We apply the sbox to the 4-bits blocs and we append the results to appli_sbox
            appli_sbox.append(format(apply_sbox(int(res_xor[i], 2), sboxes[j], i), '04b'))
        # We segment appli_sbox with 32-bits blocs to find X0, X1, X2, X3
        X0, X1, X2, X3 = segment_bits(''.join(appli_sbox), 32)
        # Linear transformation application
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
        # B formation with X0, X1, X2, X3 after linear transformation
        B = ''.join([X0, X1, X2, X3])
    # At the end of the for loop, we have B_31 that we xor with K_31
    res_xor = segment_bits(xor(B, K_i[31]), 4)
    appli_sbox = []
    for i in range(32):
        appli_sbox.append(format(apply_sbox(int(res_xor[i], 2), sboxes[31], i), '04b'))
    B_32 = xor(''.join(appli_sbox), K_i[32])
    return B_32

def encrypt(message, K):
    M = segment_bits(padding(text_to_bits(message)), 128)

    IPTable = [
        0, 32, 64, 96, 1, 33, 65, 97, 2, 34, 66, 98, 3, 35, 67, 99, 4, 36, 68, 100, 5, 37, 69, 101, 6, 38, 70, 102, 7, 39, 71, 103, 8, 40, 72, 104, 9, 41, 73, 105, 10, 42, 74, 106, 11, 43, 75, 107, 12, 44, 76, 108, 13, 45, 77, 109, 14, 46, 78, 110, 15, 47, 79, 111, 16, 48, 80, 112, 17, 49, 81, 113, 18, 50, 82, 114, 19, 51, 83, 115, 20, 52, 84, 116, 21, 53, 85, 117, 22, 54, 86, 118, 23, 55, 87, 119, 24, 56, 88, 120, 25, 57, 89, 121, 26, 58, 90, 122, 27, 59, 91, 123, 28, 60, 92, 124, 29, 61, 93, 125, 30, 62, 94, 126, 31, 63, 95, 127]
    FPTable = [
        0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124, 1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126, 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, 67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119, 123, 127]

    K_i = K_i_gen(K)

    C = []
    for i in range(len(M)):
        B_0 = permutation_initiale(IPTable, M[i])

        B_32 = B_iterations(B_0, K_i)
        
        C.append(permutation_finale(FPTable, B_32))
    return ''.join(C)
    # print("Le message chiffré est :", ''.join(C))