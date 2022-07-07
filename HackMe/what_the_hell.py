from z3 import *


def main():
    a = BitVec('a', 32)
    b = BitVec('b', 32)
    s = Solver()
    s.add(a * b == 0xddc34132)
    s.add((a ^ 0x7e) * (b + 0x10) == 0x732092be)
    s.add((a - b) & 0xfff == 0xcdf)
    s.add()
    check = s.check()
    print(check)
    print(s.model())


if __name__ == '__main__':
    main()

#  [b = 1234567890, a = 2136772529] 2136772529-1234567890
