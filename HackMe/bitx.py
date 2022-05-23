def main():
    f = open("./asset/bitx.txt", 'r')
    data = f.readlines()
    f.close()
    for i in range(len(data)):
        data[i] = data[i][35:37]

    for i in range(len(data)):
        c = 32
        while c < 127:
            #if ((c + 9) != ((data[i] & 0x55) * 2 | ((int)(data[i] & 0xaa) >> 1)))
            edx = c + 9
            eax = int(data[i], 16)
            eax = eax & 0xaa
            eax = eax >> 1
            ecx = eax
            eax = int(data[i], 16)
            eax = eax & 0x55
            eax += eax
            eax = eax | ecx

            if edx % 255 == eax % 255:
                print(chr(c), end='')
                break

            c += 1

if __name__ == '__main__':
    main()
