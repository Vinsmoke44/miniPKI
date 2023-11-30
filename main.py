from async_message import *
from crypt_decrypt import *
from verify_certificate import *
from sign_certificate import *
from proof_knowledge import *
from doc_chest import *
from key_generator import *
import time

def pading(message):
    padded_message = message + '1'
    original_length = len(message)
    padding_length = 128 - (original_length + 1) % 128
    padded_message += '0' * padding_length
    if original_length % 128 == 0:
        padded_message += '0' * 128   
    return padded_message

def text_to_bits(text):
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
    blocks[last_block_index] = pading(blocks[last_block_index])
    return blocks

def desegment(block):
    bites=""
    for i in block: 
        bites += i
    return bites

# Test pour verifier la validité des messages
# message=input("Rentrez votre message\n")
# bits=text_to_bits(message)
# block=segment(bits)
# for i in block: 
#     print(i)
# time.sleep(2)
# bites = desegment(block)
# dcrypt=bits_to_text(bites)
# print(dcrypt)

# test=input("Entrez binaire\n")
# dcode=bits_to_text(test)
# print(dcode)


