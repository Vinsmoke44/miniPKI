import struct
import sys

xFF = 0xFF
block_size = 16
key_size = 32
key = bytearray()
prekeys = [0] * 140


ip_table = [
    0, 32, 64, 96, 1, 33, 65, 97, 2, 34, 66, 98, 3, 35, 67, 99,
    4, 36, 68, 100, 5, 37, 69, 101, 6, 38, 70, 102, 7, 39, 71, 103,
    8, 40, 72, 104, 9, 41, 73, 105, 10, 42, 74, 106, 11, 43, 75, 107,
    12, 44, 76, 108, 13, 45, 77, 109, 14, 46, 78, 110, 15, 47, 79, 111,
    16, 48, 80, 112, 17, 49, 81, 113, 18, 50, 82, 114, 19, 51, 83, 115,
    20, 52, 84, 116, 21, 53, 85, 117, 22, 54, 86, 118, 23, 55, 87, 119,
    24, 56, 88, 120, 25, 57, 89, 121, 26, 58, 90, 122, 27, 59, 91, 123,
    28, 60, 92, 124, 29, 61, 93, 125, 30, 62, 94, 126, 31, 63, 95, 127
]
fp_table = [
         0,  4,  8, 12, 16, 20, 24, 28, 32,  36,  40,  44,  48,  52,  56,  60,
        64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124,
         1,  5,  9, 13, 17, 21, 25, 29, 33,  37,  41,  45,  49,  53,  57,  61,
        65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125,
         2,  6, 10, 14, 18, 22, 26, 30, 34,  38,  42,  46,  50,  54,  58,  62,
        66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126,
         3,  7, 11, 15, 19, 23, 27, 31, 35,  39,  43,  47,  51,  55,  59,  63,
        67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119, 123, 127
]

s0 = [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12]
s1 = [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4]
s2 = [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2]
s3 = [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14]
s4 = [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13]
s5 = [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1]
s6 = [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0]
s7 = [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6]
s_boxes = [s0, s1, s2, s3, s4, s5, s6, s7]

is0 = [13, 3, 11, 0, 10, 6, 5, 12, 1, 14, 4, 7, 15, 9, 8, 2]
is1 = [5, 8, 2, 14, 15, 6, 12, 3, 11, 4, 7, 9, 1, 13, 10, 0]
is2 = [12, 9, 15, 4, 11, 14, 1, 2, 0, 3, 6, 13, 5, 8, 10, 7]
is3 = [0, 9, 10, 7, 11, 14, 6, 13, 3, 5, 12, 2, 4, 8, 15, 1]
is4 = [5, 0, 8, 3, 10, 9, 7, 14, 2, 12, 11, 6, 4, 15, 13, 1]
is5 = [8, 15, 2, 9, 4, 1, 13, 14, 11, 6, 5, 3, 7, 12, 10, 0]
is6 = [15, 10, 1, 13, 5, 3, 6, 0, 4, 9, 14, 7, 2, 12, 8, 11]
is7 = [3, 0, 6, 13, 9, 14, 15, 8, 5, 12, 11, 7, 10, 1, 4, 2]
is_boxes = [is0, is1, is2, is3, is4, is5, is6, is7]

def main():
    if len(sys.argv) == 2:
        # Iterative Encryption
        test_in = bytearray([0x00] * 16)
        test_key = bytearray([0x00] * 32)
        iters = int(sys.argv[1])

        for _ in range(iters):
            set_key(test_key)
            encrypt(test_in)

        print(test_in.hex())

    elif len(sys.argv) == 6:
        # File Encryption/Decryption
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        key = bytes.fromhex(sys.argv[3])
        nonce_value = int(sys.argv[4])
        mode = sys.argv[5]

        # Read file
        try:
            with open(input_file_path, 'rb') as in_file:
                file_data = bytearray(in_file.read())
        except FileNotFoundError:
            print(f"Error: File '{input_file_path}' not found.")
            return

        # Set key
        set_key(key)

        # Setup file writing
        with open(output_file_path, 'wb') as out_file:
            iv = bytearray(struct.pack('<I', nonce_value))
            encrypt(iv)

            if mode == 'e':
                # File encryption in CBC mode
                for i in range(0, len(file_data), 16):
                    block = bytearray([0x00] * 16)

                    for n in range(16):
                        block[n] = file_data[i + n] ^ iv[n]

                    encrypt(block)
                    iv = block
                    out_file.write(block)

            elif mode == 'd':
                # File decryption in CBC mode
                for i in range(0, len(file_data), 16):
                    block = file_data[i:i + 16]
                    saved_for_iv = block.copy()

                    decrypt(block)

                    for n in range(16):
                        block[n] ^= iv[n]

                    iv = saved_for_iv
                    out_file.write(block)

            else:
                print("Error: Encrypt/Decrypt option invalid, input 'e' or 'd' as the 5th argument.")

    else:
        print("Error: Invalid number of command-line arguments.")

if __name__ == "__main__":
    main()


def set_key(self, key):
    if len(key) != self.key_size():
        self.key = bytearray(self.key_size())
        for i in range(len(key)):
            self.key[i] = key[i]
        
        # Pad key to 256-bit
        for i in range(len(key), self.key_size()):
            if i == len(key):
                # Start of padding!
                self.key[i] = 0x80
            else:
                self.key[i] = 0x00
    else:
        self.key = key

    # Prekey initialization from K
    for i in range(8):
        self.prekeys[i] = Packing.pack_int_big_endian(
            [self.key[4 * i], self.key[4 * i + 1], self.key[4 * i + 2], self.key[4 * i + 3]], 0
        )

    # Build out prekey array
    # There's a shift of 8 positions here because I build the intermediate keys in the same
    # array as the other prekeys.
    for i in range(8, len(self.prekeys)):
        phi = 0x9e3779b9
        tmp = (
            self.prekeys[i - 8]
            ^ self.prekeys[i - 5]
            ^ self.prekeys[i - 3]
            ^ self.prekeys[i - 1]
            ^ i - 8
            ^ phi
        )
        self.prekeys[i] = (tmp << 11) | (tmp >> (21))


def encrypt(text, key):
    data = init_permutation(text)
    temp = [
            data[12], data[13], data[14], data[15],
            data[8], data[9], data[10], data[11],
            data[4], data[5], data[6], data[7],
            data[0], data[1], data[2], data[3],
        ]
    data = temp
    round_key = [0] * 16

        # 32 rounds
    for i in range(32):
            round_key = get_round_key(i)
            for n in range(16):
                data[n] = data[n] ^ round_key[n]
            data = s_box(data, i)

            if i == 31:
                # For round 32, instead of a linear transform, we get the last produced round key and XOR it with the current state.
                round_key = get_round_key(32)
                for n in range(16):
                    data[n] = data[n] ^ round_key[n]
            else:
                data = linear_transform(data)

    data = final_permutation(data)

    text[0], text[1], text[2], text[3] = data[3], data[2], data[1], data[0]
    text[4], text[5], text[6], text[7] = data[7], data[6], data[5], data[4]
    text[8], text[9], text[10], text[11] = data[11], data[10], data[9], data[8]
    text[12], text[13], text[14], text[15] = data[15], data[14], data[13], data[12]


def decrypt(text, key):
    temp = [
        text[3], text[2], text[1], text[0],
        text[7], text[6], text[5], text[4],
        text[11], text[10], text[9], text[8],
        text[15], text[14], text[13], text[12],
    ]
    data = init_permutation(temp)
    round_key = get_round_key(32)
    
    for n in range(16):
        data[n] = data[n] ^ round_key[n]

    # 32 rounds in reverse
    for i in range(31, -1, -1):
        if i != 31:
            data = inv_linear_transform(data)

        data = s_box_inv(data, i)
        round_key = get_round_key(i)

        for n in range(16):
            data[n] = data[n] ^ round_key[n]

    data = final_permutation(data)

    text[0], text[1], text[2], text[3] = data[3], data[2], data[1], data[0]
    text[4], text[5], text[6], text[7] = data[7], data[6], data[5], data[4]
    text[8], text[9], text[10], text[11] = data[11], data[10], data[9], data[8]
    text[12], text[13], text[14], text[15] = data[15], data[14], data[13], data[12]


def init_permutation(data):
    output = bytearray(16)

    for i in range(128):
        # Bit permutation based on ip lookup table
        bit = (data[ip_table[i] // 8] >> (ip_table[i] % 8)) & 0x01
        if bit & 0x01 == 1:
            output[15 - (i // 8)] |= 1 << (i % 8)
        else:
            output[15 - (i // 8)] &= ~(1 << (i % 8))

    return output



def get_round_key(round):
    k0 = prekeys[4 * round + 8]
    k1 = prekeys[4 * round + 9]
    k2 = prekeys[4 * round + 10]
    k3 = prekeys[4 * round + 11]
    box = (((3 - round) % 8) + 8) % 8
    in_bytes = bytearray(16)

    for j in range(0, 32, 2):
        in_bytes[j // 2] = (
            (k0 >> j) & 0x01 |
            ((k1 >> j) & 0x01) << 1 |
            ((k2 >> j) & 0x01) << 2 |
            ((k3 >> j) & 0x01) << 3 |
            ((k0 >> (j + 1)) & 0x01) << 4 |
            ((k1 >> (j + 1)) & 0x01) << 5 |
            ((k2 >> (j + 1)) & 0x01) << 6 |
            ((k3 >> (j + 1)) & 0x01) << 7
        )

    out = s_box(in_bytes, box)
    key = bytearray(16)

    for i in range(3, -1, -1):
        for j in range(4):
            key[3 - i] |= (out[i * 4 + j] & 0x01) << (j * 2) | ((out[i * 4 + j] >> 4) & 0x01) << (j * 2 + 1)
            key[7 - i] |= ((out[i * 4 + j] >> 1) & 0x01) << (j * 2) | ((out[i * 4 + j] >> 5) & 0x01) << (j * 2 + 1)
            key[11 - i] |= ((out[i * 4 + j] >> 2) & 0x01) << (j * 2) | ((out[i * 4 + j] >> 6) & 0x01) << (j * 2 + 1)
            key[15 - i] |= ((out[i * 4 + j] >> 3) & 0x01) << (j * 2) | ((out[i * 4 + j] >> 7) & 0x01) << (j * 2 + 1)

    return init_permutation(key)


def s_box(data, round):
    to_use = s_boxes[round % 8]
    output = bytearray(block_size())

    for i in range(block_size()):
        # Break signed-ness
        curr = data[i] & 0xFF
        low4 = (curr >> 4) & 0x0F
        high4 = curr & 0x0F
        output[i] = (to_use[low4] << 4) ^ to_use[high4]

    return output

def s_box_inv(data, round):
    to_use = is_boxes[round % 8]
    output = bytearray(block_size())

    for i in range(block_size()):
        # Break signed-ness
        curr = data[i] & 0xFF
        low4 = (curr >> 4) & 0x0F
        high4 = curr & 0x0F
        output[i] = (to_use[low4] << 4) ^ to_use[high4]

    return output

def linear_transform(data):
    data = final_permutation(data)
    output = bytearray(block_size())
    buffer = struct.pack('>IIII', *struct.unpack('<IIII', data))
    
    x0, x1, x2, x3 = struct.unpack('>IIII', buffer)

    x0 = ((x0 << 13) | (x0 >> (32 - 13)))
    x2 = ((x2 << 3) | (x2 >> (32 - 3)))
    x1 = x1 ^ x0 ^ x2
    x3 = x3 ^ x2 ^ (x0 << 3)
    x1 = (x1 << 1) | (x1 >> (32 - 1))
    x3 = (x3 << 7) | (x3 >> (32 - 7))
    x0 = x0 ^ x1 ^ x3
    x2 = x2 ^ x3 ^ (x1 << 7)
    x0 = (x0 << 5) | (x0 >> (32 - 5))
    x2 = (x2 << 22) | (x2 >> (32 - 22))

    buffer = struct.pack('>IIII', x0, x1, x2, x3)
    
    output = bytearray(struct.unpack('<IIII', buffer))
    output = init_permutation(output)

    return output

def inv_linear_transform(data):
    data = final_permutation(data)
    output = bytearray(block_size())
    buffer = struct.pack('>IIII', *struct.unpack('<IIII', data))
    
    x0, x1, x2, x3 = struct.unpack('>IIII', buffer)

    x2 = (x2 >> 22) | (x2 << (32 - 22))
    x0 = (x0 >> 5) | (x0 << (32 - 5))
    x2 = x2 ^ x3 ^ (x1 << 7)
    x0 = x0 ^ x1 ^ x3
    x3 = (x3 >> 7) | (x3 << (32 - 7))
    x1 = (x1 >> 1) | (x1 << (32 - 1))
    x3 = x3 ^ x2 ^ (x0 << 3)
    x1 = x1 ^ x0 ^ x2
    x2 = (x2 >> 3) | (x2 << (32 - 3))
    x0 = (x0 >> 13) | (x0 << (32 - 13))

    buffer = struct.pack('>IIII', x0, x1, x2, x3)
    
    output = bytearray(struct.unpack('<IIII', buffer))
    output = init_permutation(output)

    return output



def final_permutation(data):
    output = bytearray(16)

    for i in range(128):
        # Bit permutation based on fp lookup table
        bit = (data[15 - fp_table[i] // 8] >> (fp_table[i] % 8)) & 0x01
        if bit & 0x01 == 1:
            output[i // 8] |= 1 << (i % 8)
        else:
            output[i // 8] &= ~(1 << (i % 8))

    return output


