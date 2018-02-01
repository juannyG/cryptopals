from ch2 import xor


def repeating_key_xor(string, key):
    result = ''
    for i in xrange(len(string)):
        result += xor(string[i].encode('hex'), key[i % len(key)].encode('hex'))
    return result

def ch5():
    """Implement repeating-key XOR

    >>> ch5()
    '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
    """
    key = 'ICE'
    with open('ch5.in') as data_f:
        return repeating_key_xor(data_f.read(), key)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
