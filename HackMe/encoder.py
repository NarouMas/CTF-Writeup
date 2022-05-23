import base64

upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lower = "abcdefghijklmnopqrstuvwxyz"


def r_rot13(s):
    return s.translate(s.maketrans(upper[13:] + upper[:13] + lower[13:] + lower[:13], upper + lower))


def r_base64(s):
    return base64.b64decode(s).decode('utf-8')


def r_hex(s):
    result = ''
    for i in range(0, len(s), 2):
        result += chr(int(s[i] + s[i + 1], 16))
    return result


def r_upsidedown(s):
    return s.translate(s.maketrans(lower + upper, upper + lower))


def main():
    f = open('./asset/encoder/flag.enc', 'r')
    data = f.read()
    f.close()
    count = 0
    while '0' <= data[0] <= '3':
        code = data[0]
        print("count:", count, "code:", code)
        data = data[1:]
        if code == '0':
            data = r_rot13(data)
        elif code == '1':
            data = r_base64(data)
        elif code == '2':
            data = r_hex(data)
        elif code == '3':
            data = r_upsidedown(data)

    print(data)


if __name__ == '__main__':
    main()
