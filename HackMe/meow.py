def main():
    f = open('./asset/meow.png', 'rb')
    data = f.read()
    png_end_data = [0xae, 0x42, 0x60, 0x82]
    for i in range(len(data)):
        flag = True
        for j in range(len(png_end_data)):
            if data[i + j] != png_end_data[j]:
                flag = False
                break
        if flag:
            zip_file = open('./asset/meow.zip', 'wb')
            for j in range(i + 4, len(data)):
                zip_file.write(data[j].to_bytes(1, byteorder='little'))
            png_file = open("./asset/pure_meow.png", 'wb')
            for j in range(i + 4):
                png_file.write(data[j].to_bytes(1, byteorder='little'))

            return


if __name__ == '__main__':
    main()