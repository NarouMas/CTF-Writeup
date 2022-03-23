file = open('./asset/xor', 'rb')
key = 'hackmepls'
data = file.readlines()
index = 0
for j in range(len(data)):
    #print(j)
    content = data[j]
    for i in range(len(content)):
        if content[i] == '\n':
            continue
        print(chr(content[i] ^ ord(key[index])), end='')
        index = (index + 1) % len(key)
