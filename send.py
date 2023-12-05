def message2bits(message):
    bits=formate(message)
    block=segment(bits)
    return block

def formate(text):
    bits = ''.join(format(ord(char), '08b') for char in text)
    return bits

def segment(bits):
    #divise en blocs de 128 bits
    blocks = [bits[i:i+128] for i in range(0, len(bits), 128)]

    # Applique le bourrage à la fin de la dernière partie si nécessaire
    last_block_index = len(blocks) - 1
    blocks[last_block_index] = pading(blocks[last_block_index])
    return blocks

def pading(message):
    padded_message = message + '1'
    original_length = len(message)
    padding_length = 128 - (original_length + 1) % 128
    padded_message += '0' * padding_length
    if original_length % 128 == 0:
        padded_message += '0' * 128   
    return padded_message