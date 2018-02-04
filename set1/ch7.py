import base64
import sys

from Crypto.Cipher import AES


def aes_ecb_128_decrypt(key, ciphertext):
    return AES.new(key).decrypt(ciphertext)


def ch7():
    """AES-128-ECB decryption wrapper

    >>> from Crypto.Cipher import AES
    >>> key = "keys" * 4
    >>> msg = "test" * 4
    >>> assert msg == aes_ecb_128_decrypt(key, AES.new(key).encrypt(msg))
    """
    key = "YELLOW SUBMARINE"
    with open("ch7.in") as data_f:
        ciphertext = base64.b64decode(data_f.read().replace('\n', ''))
        print aes_ecb_128_decrypt(key, ciphertext)

if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
    elif '--solve' in sys.argv:
        ch7()
