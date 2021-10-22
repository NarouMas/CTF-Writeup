from pwn import *
import pwn


def main():
    r = pwn.remote('ctf.hackme.quest', 7702)
    r.interactive()


if __name__ == '__main__':
    main()
