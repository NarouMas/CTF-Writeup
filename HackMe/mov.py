from pwn import *

def main():
    flag = "FLAG{"
    char_set = "0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}"
    for _ in range(60):
        for c in char_set:
            r = process("./asset/mov")
            r.recvuntil(b'Input flag: ')
            r.send((flag + c).encode('ascii'))
            res = r.recvline().decode('ascii')
            r.close()

            if 'Good flag' in res:
                find = True
                flag += c
                print("char find, current flag:", flag)
                if c == '}':
                    print("The whole flag is found:", flag)
                    return
                break

if __name__ == "__main__":
    main()
