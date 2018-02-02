from ch3 import single_byte_xor_cipher_cracker

def single_character_xor_cipher_searcher():
    """In a given file, find the line that was single byte XOR'd

    >>> single_character_xor_cipher_searcher()
    (95.86009764624164, 'Now that the party is jumping\\n')
    """
    highest_chi_2 = (0, None)
    with open('ch4.in', 'r') as data_f:
        for line in data_f.read().split('\n'):
            result = single_byte_xor_cipher_cracker(line)
            if highest_chi_2[0] < result[0]:
                highest_chi_2 = result
    return highest_chi_2

if __name__ == "__main__":
    import doctest
    doctest.testmod()
