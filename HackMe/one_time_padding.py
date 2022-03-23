import requests

url = 'https://ctf.hackme.quest/otp/?issue_otp=1'

for i in range(0, 100, 2):
    table = {}
    while len(table) != 255:
        content = requests.get(url)
        data = content.text.split('\n')
        for j in range(20):
            num = data[j][i: i+2]
            table[int(num, 16)] = 1
    for j in range(256):
        if j not in table:
            print(chr(j), end='')
            break
