def main():
    crypted = open("./asset/shuffle/crypted.txt", 'r')
    plain = open("./asset/shuffle/plain.txt", 'r')
    count_crypted = [0] * 0x7f
    count_plain = [0] * 0x7f
    table = [[] for _ in range(0x7f)]

    crypted_data = crypted.read()
    for c in crypted_data:
        count_crypted[ord(c)] += 1
    plain_data = plain.read()
    for c in plain_data:
        count_plain[ord(c)] += 1

    for i in range(0x20, 0x7f):
        if count_crypted[i] != 0:
            print(chr(i), ':', end='')
            for j in range(0x20, 0x7f):
                if count_plain[j] == count_crypted[i]:
                    print(chr(j), end=', ')
                    table[i].append(chr(j))
            print()

    recover = open("./asset/shuffle/recover.txt", "w")
    for c in crypted_data:
        if len(table[ord(c)]) == 0:
            recover.write('?')
        else:
            if len(table[ord(c)]) == 1:
                recover.write(table[ord(c)][0])
            else:
                recover.write('(')
                for i in range(len(table[ord(c)])):
                    recover.write(table[ord(c)][i])
                recover.write(')')


if __name__ == '__main__':
    main()
