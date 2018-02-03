def pkcs7_pad(msg, block_len):
    """PKCS#7 Padding implementation

    >>> pkcs7_pad("aaaa", 4)
    'aaaa'
    >>> pkcs7_pad("aaaa", 5)
    'aaaa\\x01'
    >>> pkcs7_pad("aaaabbbbc", 4)
    'aaaabbbbc\\x03\\x03\\x03'
    """
    remainder = len(msg) % block_len
    if not remainder:
        return msg
    pad_int = block_len - remainder
    str_hex_pad = ('0%x' % pad_int if pad_int < 15 else '%x' % pad_int) * pad_int
    return msg + str_hex_pad.decode('hex')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
