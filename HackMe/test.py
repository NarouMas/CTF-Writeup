import base64

s = "RkxBR3suLi4uLn0="
print(base64.b64decode(s).decode('utf-8'))