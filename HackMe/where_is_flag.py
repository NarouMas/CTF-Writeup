import re


def main():
    f = open('./asset/flag', 'r')
    data = f.read()
    f.close()
    regex = re.compile('FLAG\{\w+\}')
    match = regex.search(data)
    print(match.group(0))


if __name__ == '__main__':
    main()