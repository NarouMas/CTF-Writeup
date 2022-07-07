def main():
    f = open("./asset/big~", 'r')
    while True:
        content = f.read(16)
        if content != 'THISisNOTFLAG{}\n':
            print(content)
            content = f.read(1000)
            print(content)
            input()


if __name__ == '__main__':
    main()
