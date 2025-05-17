from pwn import *

def main():
    charset = [chr(c) for c in range(32, 128)]
    flag = ''
    while True:
        can = ""
        for c in charset:
            r = process("./asset/esrever-mv")
            data = (flag + c).encode('utf-8')
            r.send(data)
            print("data:", data)
            message = r.recv()
            r.close()
            print("message:", message)
            if message.decode() == 'Input flag: ':
                can += c
                #print("flag:", flag)
        print("flag:", flag)
        print("can:", can)  
        flag += input('intput:')

if __name__ == "__main__":
    main()
