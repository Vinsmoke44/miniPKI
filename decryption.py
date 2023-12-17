#!/bin/env/python3

def bits_to_text(bits):
	text = ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))
	return text

def permutation_finale(bloc):
    result = 0
    for i in range(128):
        # Obtient la valeur du bit à la position 
        bit = (int(bloc, 2) >> ((4 * i) % 127)) & 1
        # Place la valeur du bit à la position i dans le nouveau bloc
        result |= bit << i
    return result

C = '10000100001110001010011001111110101111000101001111000100001011011110001001111100000011100110111011100110010010101000011011111111'

B_0 = permutation_finale(C)
print(len(format(B_0, '0128b')))