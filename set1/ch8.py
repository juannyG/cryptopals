import sys

AES_BLOCK_SIZE = 16

def count_block_instances(test_block, block_set):
    """Count the number of appearances of a "block"
    in a list of blocks

    >>> count_block_instances('a', ['a', 'a', 'b', 'a'])
    3
    """
    count = 0
    for i, block in enumerate(block_set):
        count += 1 if block == test_block else 0
    return count

def test_for_aes_ecb(hex_str):
    """Test if a hex string looks like it may be the result
    of AES-128-ECB encryption

    >>> test_str = ('00' * 16) + ('01' * 16) + ('00' * 16)
    >>> test_for_aes_ecb(test_str)
    True
    >>> test_str = ('00' * 16) + ('01' * 16) + ('02' * 16)
    >>> test_for_aes_ecb(test_str)
    False
    """
    bytes = hex_str.decode('hex')
    block_count = len(bytes) / AES_BLOCK_SIZE
    blocks = [bytes[AES_BLOCK_SIZE * i:AES_BLOCK_SIZE * (i + 1)] for i in xrange(block_count)]
    for block in blocks:
        count = count_block_instances(block, blocks)
        if count > 1:
            return True
    return False

def ch8():
    hex_strings = []
    with open("ch8.in", 'r') as data_f:
        hex_strings = data_f.read().split('\n')

    for hex_str in hex_strings:
        is_ecb = test_for_aes_ecb(hex_str)
        if is_ecb:
            print hex_str


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod()
    elif '--solve' in sys.argv:
        ch8()
