from BitVector import *
import copy
import time
import binascii

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)
InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)
rc_i = ["00", "01", "02", "04", "08", "10", "20", "40", "80", "1B", "36"]
Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]
InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]


#key = bytearray.fromhex("44656372797074205461736b20536978").decode("utf-8") # "Thats my Kung Fu"
key = input("Enter Key:")
if len(key) < 16:
    key = key + "0"*(16-len(key))

start_time = time.time()
key = key.encode("utf-8").hex()
k_final = []
k_words = [[], [], [], []]
for a in range(16):
    t = int((a)/4)
    k_words[t].append(key[a*2:a*2+2])


def print_matrix(m):
    for i in range(4):
        for j in range(4):
            print(m[i][j], end="  ")
        print("\n")


def sub_byte(a):                        # a --> hex number
    b = BitVector(hexstring=a)
    int_val = b.intValue()             # Binary -> Decimal
    s = Sbox[int_val]                  # Look up from table
    s = BitVector(intVal=s, size=8)    # Decimal -> Binary(BCD)
    return s.get_bitvector_in_hex()


def inv_sub_byte(a):
    b = BitVector(hexstring=a)
    int_val = b.intValue()             # Binary -> Decimal
    s = InvSbox[int_val]                  # Look up from table
    s = BitVector(intVal=s, size=8)    # Decimal -> Binary(BCD)
    return s.get_bitvector_in_hex()


def g_func(w, i):
    # Circular Byte left shift
    w_temp = copy.deepcopy(w[0])
    for a in range(3):
        w[a] = w[a+1]
    w[3] = w_temp

    # Byte Substitute
    for a in range(4):
        w[a] = sub_byte(w[a])

    # Adding round constant
    bv1 = BitVector(hexstring=w[0])
    bv2 = BitVector(hexstring=rc_i[i])
    w[0] = (bv1^bv2).get_bitvector_in_hex()
    return w


def generate_key(w, i):
    new_key = w
    temp_w3 = copy.deepcopy(w[3])
    g_value = g_func(temp_w3, i)

    for a in range(4):
        new_key[0][a] = (BitVector(hexstring=w[0][a])^BitVector(hexstring=g_value[a])).get_bitvector_in_hex()
    for a in range(4):
        new_key[1][a] = (BitVector(hexstring=w[1][a])^BitVector(hexstring=new_key[0][a])).get_bitvector_in_hex()
    for a in range(4):
        new_key[2][a] = (BitVector(hexstring=w[2][a])^BitVector(hexstring=new_key[1][a])).get_bitvector_in_hex()
    for a in range(4):
        new_key[3][a] = (BitVector(hexstring=w[3][a])^BitVector(hexstring=new_key[2][a])).get_bitvector_in_hex()
    return new_key


k_final.append(copy.deepcopy(k_words))

for a in range(10):
    temp_key = generate_key(k_words[0:], a+1)
    k_final.append(copy.deepcopy(temp_key))

key_gen_time = time.time() - start_time


def t_matrix(m):              # Transpose Matrix
    temp_m = copy.deepcopy(m)
    for i in range(4):
        for j in range(4):
            temp_m[i][j] = m[j][i]
    return temp_m


def add_round_key(text, k):         # input --> text , key (both 4*4 matrices)
    for i in range(4):
        for j in range(4):
            bv1 = BitVector(hexstring=text[i][j])
            bv2 = BitVector(hexstring=k[i][j])
            text[i][j] = (bv1^bv2).get_bitvector_in_hex()
    return text


def shift_row(text):
    temp = copy.deepcopy(text)
    for row in range(1, 4, 1):
        for i in range(4):
            text[row][i] = temp[row][(i + row) % 4]
    return text


def inv_shift_row(text):
    temp = copy.deepcopy(text)
    for row in range(1, 4, 1):
        for i in range(4):
            text[row][i] = temp[row][(i - row) % 4]
    return text


def mix_column(text):
    const = [["02", "03", "01", "01"], ["01", "02", "03", "01"], ["01", "01", "02", "03"], ["03", "01", "01", "02"]]
    temp_text = [["00", "00", "00", "00"], ["00", "00", "00", "00"], ["00", "00", "00", "00"], ["00", "00", "00", "00"]]
    for row in range(4):
        for col in range(4):
            for i in range(4):
                AES_modulus = BitVector(bitstring='100011011')
                bv1 = BitVector(hexstring=const[row][i])
                bv2 = BitVector(hexstring=text[i][col])
                bv3 = bv1.gf_multiply_modular(bv2, AES_modulus, 8)

                temp_text[row][col] = (BitVector(hexstring=temp_text[row][col])^bv3).get_bitvector_in_hex()
    return temp_text


def inv_mix_column(text):
    const = [["0e", "0b", "0d", "09"], ["09", "0e", "0b", "0d"], ["0d", "09", "0e", "0b"], ["0b", "0d", "09", "0e"]]
    temp_text = [["00", "00", "00", "00"], ["00", "00", "00", "00"], ["00", "00", "00", "00"], ["00", "00", "00", "00"]]
    for row in range(4):
        for col in range(4):
            for i in range(4):
                AES_modulus = BitVector(bitstring='100011011')
                bv1 = BitVector(hexstring=const[row][i])
                bv2 = BitVector(hexstring=text[i][col])
                bv3 = bv1.gf_multiply_modular(bv2, AES_modulus, 8)

                temp_text[row][col] = (BitVector(hexstring=temp_text[row][col])^bv3).get_bitvector_in_hex()
    return temp_text


# Encryption
def encryption(message):  # 16 Byte message
    # global start_time
    # start_time = time.time()

    text = [[], [], [], []]
    for a in range(16):
        t = int((a) / 4)
        text[t].append(message[a*2 : a*2+2])

    #print("Plain Text:")
    #print(text)
    key0 = copy.deepcopy(k_final[0])

    key0 = t_matrix(key0)
    message = t_matrix(text)
    message = add_round_key(message, key0)

    # Round 1 to 9
    for r in range(1, 10, 1):
        # Substitute Bytes
        for i in range(4):
            for j in range(4):
                message[i][j] = sub_byte(message[i][j])

        # Shift Row
        shift_row(message)

        # Mix Column
        message = mix_column(message)

        # Add Round Key
        key_n = copy.deepcopy(k_final[r])
        key_n = t_matrix(key_n)
        message = add_round_key(message, key_n)

    # 10th round
    # Substitute Bytes
    for i in range(4):
        for j in range(4):
            message[i][j] = sub_byte(message[i][j])

    # Shift Row
    shift_row(message)

    # Add Round Key
    key_n = copy.deepcopy(k_final[10])
    key_n = t_matrix(key_n)
    message = add_round_key(message, key_n)
    message = t_matrix(message)

    msg = ""
    for i in range(4):
        for j in range(4):
            msg += message[i][j]
    return msg


# Decryption
def decryption(cipher):  # 16 Byte cypher
    # global start_time
    # start_time = time.time()

    text = [[], [], [], []]
    for a in range(16):
        t = int((a) / 4)
        text[t].append(cipher[a * 2: a * 2 + 2])

    #print("Cypher:")
    #print(cypher)
    key10 = copy.deepcopy(k_final[10])

    key10 = t_matrix(key10)
    message = t_matrix(text)
    message = add_round_key(message, key10)

    # Round 1 to 9
    for r in range(1, 10, 1):
        # Inv Shift Row
        inv_shift_row(message)

        # Inv Substitute Bytes
        for i in range(4):
            for j in range(4):
                message[i][j] = inv_sub_byte(message[i][j])

        # Add Round Key
        key_n = copy.deepcopy(k_final[10-r])
        key_n = t_matrix(key_n)
        message = add_round_key(message, key_n)

        # Inv Mix Column
        message = inv_mix_column(message)

    # 10th round
    # Shift Row
    inv_shift_row(message)

    # Substitute Bytes
    for i in range(4):
        for j in range(4):
            message[i][j] = inv_sub_byte(message[i][j])

    # Add Round Key
    key_n = copy.deepcopy(k_final[0])
    key_n = t_matrix(key_n)
    message = add_round_key(message, key_n)
    message = t_matrix(message)

    msg = ""
    for i in range(4):
        for j in range(4):
            msg += message[i][j]
    return msg


msg = input("Enter Message to Encrypt :")
start_time = time.time()
while 1:
    if len(msg) == 0:
        break
    elif len(msg) <= 16:
        msg += " "*(16-len(msg))
        msg = msg.encode("utf-8").hex()
        Cipher = encryption(msg)
        print("Cipher: ", Cipher)
        break
    else:
        temp_msg = msg[0:16]
        temp_msg = temp_msg.encode("utf-8").hex()
        Cipher = encryption(temp_msg)
        print("Cipher: ", Cipher)
        msg = msg[16:]
enc_time = time.time() - start_time

c = int(input("Want to encrypt a file?(0/1): "))
if c == 1:
    filename = input("Enter a filename to encrypt: ")
    with open(filename, 'rb') as f:
        content = f.read()
    msg = binascii.hexlify(content).hex()

    cipher_file = open("out1.txt", "w")
    cipher_file.close()
    start_time = time.time()
    while 1:
        if len(msg) == 0:
            break
        elif len(msg) <= 16:
            msg += " "*(16-len(msg))
            msg = msg.encode("utf-8").hex()
            # print(msg)
            Cipher = encryption(msg)

            cipher_file = open("out1.txt", "a")
            cipher_file.write(Cipher)
            cipher_file.close()
            # print("Cipher: ", Cipher)
            break
        else:
            temp_msg = msg[0:16]
            temp_msg = temp_msg.encode("utf-8").hex()
            # print(temp_msg)
            Cipher = encryption(temp_msg)

            cipher_file = open("out1.txt", "a")
            cipher_file.write(Cipher)
            cipher_file.close()
            # print("Cipher: ", Cipher)
            msg = msg[16:]
    enc_time = time.time() - start_time


Cipher = input("Enter Ciphertext in hex(n * 16 byte) :")
start_time = time.time()
while 1:
    if len(Cipher) == 0:
        break
    elif len(Cipher) == 32:
        msg = decryption(Cipher)
        print("Msg in hex: ", msg)
        print("In ASCII: ", bytearray.fromhex(msg).decode("utf-8"))
        break
    else:
        temp_cipher = Cipher[0:32]
        msg = decryption(temp_cipher)
        print("Msg in hex: ", msg)
        print("In ASCII: ", bytearray.fromhex(msg).decode("utf-8"))
        Cipher = Cipher[32:]
dec_time = time.time() - start_time


c = int(input("Want to decrypt a file?(0/1): "))
if c == 1:
    file = input("Enter filename(.txt) to decrypt :")
    start_time = time.time()
    plain_text = open("out2.txt", "w")
    plain_text.close()

    Cipher = open(file, "r").read()
    while 1:
        if len(Cipher) == 0:
            break
        elif len(Cipher) == 32:
            msg = decryption(Cipher)
            #print(msg)

            msg = binascii.unhexlify(msg).hex()
            msg = bytes.fromhex(msg)
            plain_text = open("out2.txt", "ab")
            plain_text.write(msg)
            plain_text.close()
            break
        else:
            temp_cipher = Cipher[0:32]
            msg = decryption(temp_cipher)
            #print(msg)

            msg = binascii.unhexlify(msg).hex()
            msg = bytes.fromhex(msg)
            plain_text = open("out2.txt", "ab")
            plain_text.write(msg)
            plain_text.close()
            Cipher = Cipher[32:]
    dec_time = time.time() - start_time

print("\n\nTime for Key Gen: ", key_gen_time)
print("Time for encryption: ", enc_time)
print("Time for decryption: ", dec_time)
