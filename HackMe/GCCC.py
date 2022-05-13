from z3 import *


def main():
    data = bytearray([164, 25, 4, 130, 126, 158, 91, 199, 173, 252, 239, 143, 150,
                          251, 126, 39, 104, 104, 146, 208, 249, 9, 219, 208, 101, 182, 62, 92, 6, 27, 5, 46])
    chrs = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ{} ')
    s = Solver()
    result = BitVec('result', 32 + 8)
    num = 0

    for i in range(32):
        c = data[i] ^ Extract(i + 7, i, result) ^ num
        if i < 5:
            x = list("FLAG{")
            s.add(c == ord(x[i]))
        elif i == 31:
            s.add((c == ord('}')))
        else:
            s.add(Or([c == ord(x) for x in chrs]))
        num = num ^ data[i]

    if s.check().__str__() == 'sat':
        print(s.model())
    else:
        print('no ans')


if __name__ == '__main__':
    main()

# reference: https://blog.maple3142.net/2020/07/23/hackme-ctf-experience-and-hints/#gccc
