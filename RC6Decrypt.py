

def decrypt(esentence, s):

    cipher = int((len(esentence) / 4)) * [0];
    num = 0
    for i in range(0, len(cipher)):
        try:
            num2 = esentence[num] & 4294967295
        except:
            num2 = ord(esentence[num]) & 4294967295
        num += 1
        try:
            num3 = esentence[num] & 4294967295
        except:
            num3 = ord(esentence[num]) & 4294967295
        num += 1
        num4 = num3 << 8
        try:
            num5 = esentence[num] & 4294967295
        except:
            num5 = ord(esentence[num]) & 4294967295
        num += 1
        num6 = num5 << 16
        try:
            num7 = esentence[num] & 4294967295
        except:
            num7 = ord(esentence[num]) & 4294967295
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
    C = (C - s[2 * r + 3]) % modulo
    A = (A - s[2 * r + 2]) % modulo
    for j in range(1, r + 1):
        i = r + 1 - j
        (A, B, C, D) = (D, A, B, C)
        u_temp = (D * (2 * D + 1)) % modulo
        u = ROL(u_temp, lgw, 32)
        t_temp = (B * (2 * B + 1)) % modulo
        t = ROL(t_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        C = (ROR((C - s[2 * i + 1]) % modulo, tmod, 32) ^ u)
        A = (ROR((A - s[2 * i]) % modulo, umod, 32) ^ t)
    D = (D - s[1]) % modulo
    B = (B - s[0]) % modulo
    orgi = [A, B, C, D]

    dec = ""
    for i in range(0, len(esentence)):
        dec += chr(orgi[int(i / 4)] >> i % 4 * 8 & 255)

    return dec


def RC6Decrypt(data, key):
    if len(key) < 16:
        key = key + " " * (16 - len(key))
    key = key[:16]
    s = generateKey(key)

    full_data = ""
    data_len = len(data)
    tracker = 0

    while data_len > 16:
        cipher = decrypt(data[tracker:tracker + 16], s)
        full_data += cipher
        tracker += 16
        data_len -= 16
    if data_len > 0:
        cipher = decrypt(data[tracker:], s)
        full_data += cipher
    return full_data
