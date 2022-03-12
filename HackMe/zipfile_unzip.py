import os
import shutil
import zipfile


def extract_ori_file():
    while True:
        zf = zipfile.ZipFile('./zip/zipfile.zip', 'r')
        zf.extractall()
        zf.close()
        os.remove('./zip/zipfile.zip')
        os.replace("./zipfile.zip", "./zip/zipfile.zip")


def extract_multi_layer_file():
    zf = zipfile.ZipFile('./zip/zipfile.zip', 'r')
    d = zf.namelist()
    for i in range(len(d)):
        data = zf.read(d[i])
        #print(data)
        f = open('./zip/extract/' + str(i) + '.zip', 'wb')
        f.write(data)
        f.close()
    for i in range(len(d)):
        zf = zipfile.ZipFile('./zip/extract/' + str(i) + '.zip', 'r')
        data = zf.read(zf.namelist()[0])
        os.mkdir('./zip/extract/' + str(i))
        f = open('./zip/extract/' + str(i) + '/' + str(i) + '.zip', 'wb')
        f.write(data)
        f.close()


def deal_with_zipfile():
    target_zip_file = zipfile.ZipFile('./zip/zipfile.zip', 'r')
    flag = ''

    # because the dir in the zip file contain with 8 bit 2 binary number
    for i in range(256):
        # 0 -> 00000000
        target_name = bin(i)[2:].zfill(8)
        # 01010101 -> 0/1/0/1/0/1/0/1
        target_name = '/'.join(target_name)

        #print(target_name)
        print('[', end='')
        little_flag = []
        for info in target_zip_file.infolist():
            if target_name != info.filename[-18:-3]:
                continue

            # read 0/1/0/1/0/1/0/1PK and create temp file
            data = target_zip_file.read(info)
            f = open('./temp', 'wb')
            f.write(data)
            f.close()

            target = './temp'
            # unzip the first zip
            zfile = zipfile.ZipFile(target, 'r')
            # print(zfile.namelist())    # file name like 'Î¨ä·¼ºÔ½¤\x8bÒ±ÂÄ\x87\x9fÄ\x9c\x90'
            for filename in zfile.namelist():
                d = zfile.read(filename)
                f2 = open('./temp2', 'wb')
                f2.write(d)
                f2.close()

            # second zip
            zfile = zipfile.ZipFile('./temp2', 'r')
            d = []
            dd = []
            for info_ in zfile.infolist():
                d.append(zfile.read(info_))

            #print(d)
            for j in range(len(d)):
                dd.append([])
                for k in range(len(d[j])):
                    dd[j].append(d[j][k])
            #print(dd)

            s = []
            for j in range(len(dd[0])):
                t = 0
                for k in range(len(dd)):
                    t = t ^ d[k][j]

                s.append(t)
            for j in range(len(s)):
                print(chr(s[j]), end='')
            print(',', end='')

        print(']')


def deal_output():
    f = open('./zip/output.txt', 'r')
    data = f.readlines()
    f.close()
    #print(data)
    for i in range(len(data)):
        data[i] = data[i][1:-2]
        s = data[i].split(',')
        print(s[1], end='')


def main():
    extract_ori_file()
    deal_with_zipfile()
    deal_output()


if __name__ == '__main__':
    main()
