crc32_tab = []
hashes = []


def main():
    global crc32_tab, hashes
    f = open("./asset/ccc/crc32_tab.txt", "r")
    content = f.readlines()
    f.close()
    for i in range(len(content)):
        data = content[i]
        data = data[38:]
        data = data.split(',')
        for j in range(3):
            crc32_tab.append(int(data[j][:-1], 16))
        crc32_tab.append(int(data[3][:-2], 16))
    f = open('./asset/ccc/hashes.txt', 'r')
    content = f.readlines()
    f.close()
    for i in range(len(content)):
        data = content[i]
        data = data[38:]
        data = data.split(',')
        for j in range(3):
            hashes.append(int(data[j][:-1], 16))
        hashes.append(int(data[3][:-2], 16))

    buffer = ''
    a = b = c = 32
    i = 3
    j = 0
    while i < 0x2b:
        iVar1 = crc32(0, buffer + chr(a) + chr(b) + chr(c), i)
        if iVar1 != hashes[j]:
            c += 1
            if c == 127:
                c = 0
                b += 1
            if b == 127:
                b = 0
                a += 1
            if a == 127:
                a = 0
                print('error')
                return

            continue
        j += 1
        i += 3
        buffer = buffer + chr(a) + chr(b) + chr(c)
        a = b = c = 32
        print(buffer)
    print(buffer)


def xor(a, b, last_8_bit=False):
    result = ''
    for i in range(len(b)):
        if a[i] == b[i]:
            result += '0'
        else:
            result += '1'
    if last_8_bit:
        return int(result[-8:], 2)
    return int(result, 2)


def inverse(a):
    result = ''
    for i in range(len(a)):
        if a[i] == '0':
            result += '1'
        else:
            result += '0'
    return result


def right_shift_8(a):
    a = list(a)
    sign = a[0]
    j = len(a) - 1
    for i in range(len(a) - 8):
        a[j] = a[j - 8]
        j -= 1
    for i in range(8):
        a[i] = '0'
    return ''.join(a)


def crc32(num, buffer, index):
    global crc32_tab, hashes
    num = '1' * 32
    i = 0
    while index != 0:
        num = xor("{:032b}".format(crc32_tab[xor("{:032b}".format(ord(buffer[i])), num, True)]), (right_shift_8(num)))
        num = "{:032b}".format(num)

        index -= 1
        i += 1
    return int(inverse(num), 2)


if __name__ == '__main__':
    main()
