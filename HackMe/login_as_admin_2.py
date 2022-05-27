import base64


def main():
    signature = b"2bcf1ad871b860ae8762d9e7491978ac"
    data = b"name=guest&admin=0" + bytes([0x80, 0x00, 0x00, 0x00, 0x00, 0x00,
                                          0x90, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) + b"&admin=1"
    data = signature + b"#" + data
    encode = base64.b64encode(data)
    print(encode)


if __name__ == "__main__":
    main()
