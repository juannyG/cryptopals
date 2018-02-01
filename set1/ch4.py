from ch3 import single_byte_xor_cipher_cracker

def single_character_xor_cipher_searcher():
    """In a given file, find the line that was single byte XOR'd

    >>> single_character_xor_cipher_searcher()
    Now that the party is jumping
    <BLANKLINE>
    """
    with open('ch4.in', 'r') as data_f:
        for line in data_f.read().split('\n'):
            result = single_byte_xor_cipher_cracker(line)
            if result:
                print result

if __name__ == "__main__":
    import doctest
    doctest.testmod()
