def rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def padding(data):
    # Ajoute le bit '1' suivi de zéros jusqu'à la longueur correcte
    padding = b"\x80" + b"\x00" * (63 - (len(data) + 8) % 64)
    
    # Ajoute la longueur du message original en bits
    length_bits = (8 * len(data)).to_bytes(8, byteorder='big')
    
    padded_data = data + padding + length_bits
    return padded_data

def split_blocks(padded_data):
    return [padded_data[i : i + 64] for i in range(0, len(padded_data), 64)]

def expand_block(block):
    w = [0] * 80
    for i in range(16):
        start = i * 4
        w[i] = int.from_bytes(block[start:start+4], byteorder='big')

    for i in range(16, 80):
        w[i] = rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

    return w

def final_hash(data):
    padded_data = padding(data)
    blocks = split_blocks(padded_data)

    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    for block in blocks:
        expanded_block = expand_block(block)
        a, b, c, d, e = h

        for i in range(80):
            if 0 <= i < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i < 80:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b, c, d, e = (
                rotate(a + f + e + k + expanded_block[i], 5) & 0xFFFFFFFF,
                a,
                rotate(b, 30),
                c,
                d,
            )

        h = (
            (h[0] + a) & 0xFFFFFFFF,
            (h[1] + b) & 0xFFFFFFFF,
            (h[2] + c) & 0xFFFFFFFF,
            (h[3] + d) & 0xFFFFFFFF,
            (h[4] + e) & 0xFFFFFFFF,
        )

    return ("{:08x}" * 5).format(*h)

def sha1(text):
    hash_input = bytes(text, "utf-8")
    return final_hash(hash_input)

# Example generation hash
# text_to_hash = "test"
# result_hash = sha1(text_to_hash)
# print(result_hash)
