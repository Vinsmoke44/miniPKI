def bits2message(bits):
    bites = desegment(bits)
    dcrypt=deformate(bites)
    return dcrypt

def deformate(bits):
    text = ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))
    return text

def desegment(block):
    bites=""
    for i in block: 
        bites += i
    return bites