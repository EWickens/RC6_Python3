import struct


def encrypt(sentence, s):
    cipher = int((len(sentence) / 4)) * [0];
    num = 0
    for i in range(0, len(cipher)):
        try:
            num2 = sentence[num] & 4294967295
        except:
            num2 = ord(sentence[num]) & 4294967295
        num += 1
        try:
            num3 = sentence[num] & 4294967295
        except:
            num3 = ord(sentence[num]) & 4294967295
        num += 1
        num4 = num3 << 8
        try:
            num5 = sentence[num] & 4294967295
        except:
            num5 = ord(sentence[num]) & 4294967295
        num += 1
        num6 = num5 << 16
        try:
            num7 = sentence[num] & 4294967295
        except:
            num7 = ord(sentence[num]) & 4294967295
        num += 1
        num8 = num7 << 24
        cipher[i] = (num2 | num4 | num6 | num8)

    A = cipher[0]
    B = cipher[1]
    C = cipher[2]
    D = cipher[3]

    r = 20
    w = 32
    modulo = 2 ** w
    lgw = 5
    B = (B + s[0]) % modulo
    D = (D + s[1]) % modulo
    for i in range(1, r + 1):
        t_temp = (B * (2 * B + 1)) % modulo
        t = ROL(t_temp, lgw, 32)
        u_temp = (D * (2 * D + 1)) % modulo
        u = ROL(u_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        A = (ROL(A ^ t, umod, 32) + s[2 * i]) % modulo
        C = (ROL(C ^ u, tmod, 32) + s[2 * i + 1]) % modulo
        (A, B, C, D) = (B, C, D, A)
    A = (A + s[2 * r + 2]) % modulo
    C = (C + s[2 * r + 3]) % modulo
    cipher = [A, B, C, D]

    dec = b""
    for i in range(0, len(sentence)):
        dec += struct.pack('B', (cipher[int(i / 4)] >> i % 4 * 8 & 255))

    return dec


def RC6Encrypt(data, key):
    if len(key) < 16:
        key = key + " " * (16 - len(key))
    key = key[:16]
    s = generateKey(key)

    full_data = b""
    data_len = len(data)
    tracker = 0

    while data_len > 16:
        cipher = encrypt(data[tracker:tracker + 16], s)
        full_data += cipher
        tracker += 16
        data_len -= 16

    if data_len > 0:
        cipher = encrypt(data[tracker:], s)
        full_data += cipher
    return full_data
