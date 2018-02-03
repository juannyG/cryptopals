import base64

from operator import itemgetter

from ch2 import xor
from ch3 import single_byte_xor_cipher_cracker

def hamming_distance(str1, str2):
    """Compute the edit/Hamming distance between two equal length strings

    >>> hamming_distance('this is a test', 'wokka wokka!!!')
    37
    """
    result = int(xor(str1.encode('hex'), str2.encode('hex')), 16)
    distance = 0
    while result:
        distance += result & 1
        result >>= 1
    return int(distance)

def guess_keysize(ciphertext_str):
    '''For a given cipher, return a guess of the keysize

    >>> guess_keysize("can you guess the key size can you guess can you guess the key size")
    10
    '''
    guesses = ()
    for keysize in xrange(2, 41):
        guess = hamming_distance(ciphertext_str[0:keysize], ciphertext_str[keysize:keysize*2])
        guesses += ((keysize, guess / keysize),)
    return sorted(guesses, key=itemgetter(1))[0][0]

def transpose_blocks(ciphertext_str, keysize):
    """Group index i of blocks into a new block, for all 0 <= i < keysize

    >>> transpose_blocks("abcabcabc", 3)
    ['aaa', 'bbb', 'ccc']
    """
    keysize_blocks = [
        ciphertext_str[keysize * i:keysize * (i + 1)]\
        for i in xrange(len(ciphertext_str) / keysize + 1)
    ]

    return [
        ''.join(
            keysize_blocks[i][j] if len(keysize_blocks[i]) > j else ''\
            for i in xrange(len(keysize_blocks))
        ) for j in xrange(keysize)
    ]

def ch6():
    """Challenge 6

    >>> ch6()
    """
    ciphertext_str = ''
    with open('ch6.in', 'r') as data_f:
        ciphertext_str = base64.b64decode(data_f.read().replace('\n', ''))

    # Fix this...
    #keysize = guess_keysize(ciphertext_str)
    keysize = 29
    transposed_blocks = transpose_blocks(ciphertext_str, keysize)
    print transposed_blocks[0].encode('hex')
    #print single_byte_xor_cipher_cracker(transposed_blocks[0].encode('hex'))
    for tb in transposed_blocks:
        result = single_byte_xor_cipher_cracker(tb.encode('hex'))
        print result, tb.encode('hex')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
