import queue

def main():
    f = open("./asset/map", 'rb')
    data = f.read()
    f.close()
    qu = queue.Queue()
    qu.put(('', 0))
    while not qu.empty():
        flag, n = qu.get()
        for c in range(32, 128):
            v = (data[(n << 9) + (4 * c)]) + (data[(n << 9) + (4 * c) + 1] << 8)
            if v != 0:
                if v == 0xffff:
                    print("Find flag:", flag + chr(c))
                    exit(0)
                qu.put((flag + chr(c), v))
                print(f"cur:{flag + chr(c)}, data:{v}")

if __name__ == '__main__':
    main()
