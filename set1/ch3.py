import collections
import operator

from ch2 import xor

COMMON_LETTERS = [' ', 'E','A','O','I','N','S', 'H', 'R', 'D', 'L', 'U']


def single_byte_xor(string, byte):
    """XOR a single byte with a target hex string

    To ensure the result is the same length as the provided string,
    we XOR each byte individually.

    >>> single_byte_xor("00ff00ff", "ff")
    'ff00ff00'

    >>> single_byte_xor("ffff", "ff")
    '0000'
    """
    r = ''
    for i in xrange(0, len(string), 2):
        r += xor(string[i:i+2], byte)
    return r

def compute_character_frequency(string):
    '''Compute character frequencies in a string.

    Returns a sorted descending list of tuples.

    >>> compute_character_frequency('abcaab')
    [('a', 3), ('b', 2), ('c', 1)]
    '''
    chr_freq = collections.defaultdict(int)
    for c in string:
        chr_freq[c] += 1
    return sorted(chr_freq.items(), key=operator.itemgetter(1), reverse=True)

def _all_bytes_are_printable(frequency_tuple):
    for k, _ in frequency_tuple:
        k_int = int(k.encode('hex'), 16)
        if (k_int < 32 or k_int > 127) and k_int != 10:
            return False
    return True

def single_byte_xor_cipher_cracker(hex_str):
    '''Crack a hex string that has been XOR'd with a single byte

    >>> single_byte_xor_cipher_cracker('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    "Cooking MC's like a pound of bacon"
    '''
    base_freq = compute_character_frequency(hex_str.decode('hex'))
    for i in xrange(256):
        test_key = '%x' % i
        test_crack = single_byte_xor(hex_str, test_key)

        test_crack_str = test_crack.decode('hex')
        chr_freq = compute_character_frequency(test_crack_str)
        if chr_freq[0][0].upper() in COMMON_LETTERS:
            if _all_bytes_are_printable(chr_freq) and chr_freq[0][1]/float(len(test_crack_str)) > 0.15:
                return test_crack_str

if __name__ == "__main__":
    import doctest
    doctest.testmod()
