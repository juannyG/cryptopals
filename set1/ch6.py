import base64
import collections

from operator import itemgetter

from ch2 import xor
from ch3 import single_byte_xor_cipher_cracker
from ch5 import repeating_key_xor

def hamming_distance(str1, str2):
    """Compute the edit/Hamming distance between two equal length strings

    >>> hamming_distance('this is a test', 'wokka wokka!!!')
    37
    >>> hamming_distance("001506".decode('hex'), "130e07".decode("hex"))
    8
    """
    result = int(xor(str1.encode('hex'), str2.encode('hex')), 16)
    distance = 0
    while result:
        distance += result & 1
        result >>= 1
    return int(distance)

def generate_potential_keysizes(ciphertext_str):
    '''Return a list of the most likely keysizes for a given
    ciphertext whose length N >= 160. The integer result of
    the normalized hamming distances provides the grouping of
    keysize candidates.

    >>> keysize_space = [i for i in xrange(2, 41)]
    >>> assert generate_potential_keysizes("a" * 160) == keysize_space
    '''
    guesses = collections.defaultdict(list)
    for keysize in xrange(2, 41):
        dist1 = hamming_distance(ciphertext_str[0:keysize], ciphertext_str[keysize:keysize*2])
        dist2 = hamming_distance(ciphertext_str[keysize*2:keysize*3], ciphertext_str[keysize*3:keysize*4])
        avg_dist = (dist1 + dist2) / (2 * keysize)
        guesses[int(avg_dist)].append(keysize)
    return sorted(guesses.items(), key=itemgetter(0))[0][1]

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

def find_repeating_key(ciphertext_str, potential_keysizes):
    """Find the repeating key by transposing the blocks of length keysize and
    solving the single byte key solution of the transposition.

    >>> find_repeating_key('abcdefghijk', [2,4])
    '\\x04\\x07'
    """
    for possible_keysize in potential_keysizes:
        keysize = possible_keysize
        single_char_cracks = []
        transposed_blocks = transpose_blocks(ciphertext_str, keysize)
        for tb in transposed_blocks:
            single_char_cracks.append(single_byte_xor_cipher_cracker(tb.encode('hex')))

        if all(single_char_cracks):
            return keysize, ''.join(single_char_cracks[i][2].decode('hex') for i in xrange(keysize))
    return None, None

def ch6():
    ciphertext_str = ''
    with open('ch6.in', 'r') as data_f:
        ciphertext_str = base64.b64decode(data_f.read().replace('\n', ''))

    keysize = None
    potential_keysizes = generate_potential_keysizes(ciphertext_str)
    keysize, repeating_key = find_repeating_key(ciphertext_str, potential_keysizes)

    if keysize and repeating_key:
        print "(keysize, repeating_key) = ({}, {})".format(keysize, repeating_key)
        return repeating_key_xor(ciphertext_str, repeating_key).decode('hex')


if __name__ == "__main__":
    import doctest
    import sys
    if '--solve' in sys.argv:
        solution = ch6()
        if '--verbose' in sys.argv:
            print solution
    elif '--test' in sys.argv:
        doctest.testmod()
