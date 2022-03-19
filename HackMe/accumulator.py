def main():
    f = open('./asset/accumulator.txt', 'r')
    content = f.readlines()
    temp = [0] * len(content)
    data = [0] * (len(content) // 4)
    for i in range(len(content)):
        ch = content[i][43:46]
        if ch.endswith('h'):
            ch = ch[:-1]
        temp[i] = int(ch, 16)

    i = 0
    j = 0
    while i < len(temp):
        data[j] = temp[i] + (temp[i + 1] << 8)
        i += 4
        j += 1

    for i in range(1, len(data)):
        print(chr(data[i] - data[i - 1]), end='')


if __name__ == '__main__':
    main()