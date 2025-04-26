def main():
    f = open('./asset/sha256sum.txt')
    content = f.readlines()
    print(content[0][18:66])
    for line in content:
        data = line[18:66]
        i = 0
        while i < len(data):
            s = data[i:i+2]
            print(chr(int(s, 16)), end='')
            #input()
            i += 3


if __name__ == '__main__':
    main()
