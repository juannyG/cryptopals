import collections
import operator
import string

from ch2 import xor

ENGLISH_CHAR_FREQ = {
    'E': 12.49, 'T': 9.28, 'A': 8.04, 'O': 7.64, 'I': 7.57, 'N': 7.23, 'S': 6.51,
    'H': 5.05, 'R': 6.28, 'D': 3.82, 'L': 4.07, 'C': 3.34, 'U': 2.73, 'M': 2.51,
    'W': 1.68, 'F': 2.40, 'G': 1.87, 'Y': 1.66, 'P': 2.14, 'B': 1.48, 'V': 1.05,
    'K': 0.54, 'J': 0.16, 'X': 0.23, 'Q': 0.12, 'Z': 0.09,
    ' ': 13.00,
}

ACCEPTED_CHARS = ENGLISH_CHAR_FREQ.keys()


def single_byte_xor(target_str, byte):
    """XOR a single byte with a target hex string

    To ensure the result is the same length as the provided string,
    we XOR each byte individually.

    >>> single_byte_xor("00ff00ff", "ff")
    'ff00ff00'

    >>> single_byte_xor("ffff", "ff")
    '0000'
    """
    r = ''
    for i in xrange(0, len(target_str), 2):
        r += xor(target_str[i:i+2], byte)
    return r

def compute_character_frequency(target_str):
    '''Compute character frequencies in a string.

    Returns a sorted descending list of tuples.

    >>> compute_character_frequency('abcaab')
    [('a', 3), ('b', 2), ('c', 1)]
    '''
    chr_freq = collections.defaultdict(int)
    for c in target_str:
        chr_freq[c.lower()] += 1
    return sorted(chr_freq.items(), key=operator.itemgetter(1), reverse=True)

def chi_2(observed_freqs, str_len):
    chi_2_res = 0
    if not all(c in string.printable[:-2] for c, _ in observed_freqs):
        return 0

    for char, observed_freq in observed_freqs:
        if not ENGLISH_CHAR_FREQ.get(char.upper()):
            continue
        obs_freq_rate = observed_freq/float(str_len)
        exp_freq_rate = ENGLISH_CHAR_FREQ.get(char.upper())
        chi_2_res += (obs_freq_rate - exp_freq_rate)**2 / exp_freq_rate
    return chi_2_res

def single_byte_xor_cipher_cracker(hex_str):
    '''Crack a hex string that has been XOR'd with a single byte using frequency analysis
    and the chi-squared test: https://en.wikipedia.org/wiki/Pearson's_chi-squared_test.

    >>> x = single_byte_xor_cipher_cracker('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    >>> int(x[0]), x[1], x[2]
    (85, "Cooking MC's like a pound of bacon", '58')
    '''
    chi_2_results = [[0]]
    target_len = len(hex_str) / 2
    for i in xrange(256):
        test_key = '%x' % i
        test_crack_str = single_byte_xor(hex_str, test_key).decode('hex')
        observed_freqs = compute_character_frequency(test_crack_str)
        chi_2_res = chi_2(observed_freqs, target_len)
        if chi_2_res:
            chi_2_results.append((chi_2_res, test_crack_str, test_key),)
    return sorted(chi_2_results, key=operator.itemgetter(0), reverse=True)[0]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
