# rotate right input x, by n bits
def ROR(x, n, bits=32):
    mask = (2 ** n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))


# rotate left input x, by n bits
def ROL(x, n, bits=32):
    return ROR(x, bits - n, bits)


def ConvBytesToWords(key):
    array = 4 * [0]
    i = 0
    num = 0
    while i < 4:
        num2 = key[num] & 4294967295
        num += 1
        num3 = key[num] & 4294967295
        num += 1
        num4 = num3 << 8
        num5 = key[num] & 4294967295
        num += 1
        num6 = num5 << 16
        num7 = key[num] & 4294967295
        num += 1
        num8 = num7 << 24
        array[i] = (num2 | num4 | num6 | num8)
        i += 1
    return array


def generateKey(userkey):
    t = 44
    w = 32
    modulo = 2 ** w
    encoded = ConvBytesToWords(userkey)
    enlength = len(encoded)

    s = t * [0]
    s[0] = 0xB7E15163
    for i in range(1, t):
        s[i] = (s[i - 1] + 0x9E3779B9) % (2 ** w)

    v = 3 * max(enlength, t)
    A = B = i = j = 0

    for index in range(0, v):
        A = s[i] = ROL((s[i] + A + B) % modulo, 3, 32)
        B = encoded[j] = ROL((encoded[j] + A + B) % modulo, (A + B) % 32, 32)
        i = (i + 1) % t
        j = (j + 1) % enlength
    return s
