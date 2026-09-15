
poly = {
    "crc-3": "1011",
    "crc-4": "10011",
    "crc-8": "100000111",
    "crc-32": "100000100110000010001110110110111"
}

def crc_remainder(data, key):
    data = list(data)
    n = len(key)
    for i in range(len(data) - n + 1):
        if data[i] == '1':
            for j in range(n):
                data[i+j] = '1' if data[i+j] != key[j] else '0'
    return ''.join(data[-(n-1):])

x = input("select one(crc-3,crc-4,crc-8,crc-32): ").strip().lower()

if x in poly:
    key = poly[x]
    text = input("enter text: ") or "Hello"
    data = ''.join(format(ord(c), '08b') for c in text)   # text -> bits
    padded = data + '0' * (len(key) - 1)
    remainder = crc_remainder(padded, key)
    codeword = data + remainder

    print("data bits:", data)
    print("crc bits :", remainder)
    print("codeword :", codeword)
else:
    print("ERROR WRONG RESPONSE DETECTED")