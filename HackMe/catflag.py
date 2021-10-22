from pwn import *
import pwn


def main():
    r = pwn.remote('ctf.hackme.quest', 7709)
    r.interactive()


if __name__ == '__main__':
    main()