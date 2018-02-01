def xor(x, y):
    """Take two equal length hex strings and XOR them

    >>> xor('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965')
    '746865206b696420646f6e277420706c6179'

    >>> xor('10', '11')
    '01'
    """
    result = int(x, 16) ^ int(y, 16)
    return '{}'.format('0%x' % result if result < 16 else '%x' % result)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
