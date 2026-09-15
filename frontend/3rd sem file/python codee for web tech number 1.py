def crc(data, generator):
    data = list(map(int, data))
    gen = list(map(int, generator))
    n = len(gen) - 1

    data += [0] * n

    for i in range(len(data) - n):
        if data[i]:
            for j in range(len(gen)):
                data[i + j] ^= gen[j]

    return ''.join(map(str, data[-n:]))


generators = {
    3: "1011",
    4: "10011",
    8: "100000111",
    32: "100000100110000010001110110110111"
}


data = input("Enter binary data or a word: ")

if all(c in "01" for c in data):
    binary = data
else:
    binary = ''.join(format(ord(c), '08b') for c in data)

print("\nBinary Data:", binary)

print("\nSelect CRC:")
print("1. CRC-3")
print("2. CRC-4")
print("3. CRC-8")
print("4. CRC-32")

choice = int(input("Enter your choice: "))

if choice not in [1, 2, 3, 4]:
    print("Invalid choice")
else:
    crc_size = [3, 4, 8, 32][choice - 1]
    generator = generators[crc_size]

    remainder = crc(binary, generator)
    codeword = binary + remainder

    print("\n----- CRC RESULT -----")
    print("Input:", data)
    print("Binary Data:", binary)
    print("CRC:", "CRC-" + str(crc_size))
    print("Generator:", generator)
    print("CRC Remainder:", remainder)
    print("Codeword:", codeword)
    