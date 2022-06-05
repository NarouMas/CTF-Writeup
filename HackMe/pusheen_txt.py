def main():
    f = open('./asset/pusheen.txt', 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    i = 0
    result = ''
    while i < len(data):
        if data[i + 8][10] == ' ':
            result += '0'
        else:
            result += '1'
        i += 16
    print(result)


if __name__ == '__main__':
    main()
