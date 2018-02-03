import base64

from Crypto.Cipher import AES


def ch7():
    key = "YELLOW SUBMARINE"
    with open("ch7.in") as data_f:
        ciphertext = base64.b64decode(data_f.read().replace('\n', ''))
        print AES.new(key).decrypt(ciphertext)

if __name__ == '__main__':
    ch7()
