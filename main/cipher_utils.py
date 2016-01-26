
import sys
import argparse

KEY = [1, 1, 1, 1, 1, 1, 1, 1]
SPACE = [0, 0, 1, 0, 0, 0, 0, 0]

class BlockObject:

    def __init__(self, bit_string):
        """
        :param char_string: incoming string to be converted into bits
        :return: sets self.string and self.bit_string accordingly
        """
        self.bit_string = bit_string

class FormatError(Exception):
    """Base class for exceptions in this module"""
    pass

def read_file(filename):
    data = None
    try:
        with open(filename, 'r') as file_read:
            data = file_read.read()
    except IOError, e:
        sys.stderr('File {0} has occured an error:'.format(filename, e))
    return data

def write_file(filename, data):
    try:
        with open(filename, 'w') as file_write:
            file_write.write(data)
    except IOError, e:
        sys.stderr('File {0} has occured an error:'.format(filename, e))

def tobits(raw_string):

    if not isinstance(raw_string, basestring):
        raise FormatError('This is not a correctly formatted string')

    result = []
    for c in raw_string:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def split(bits, size):
    return [bits[i:i+size] for i in xrange(0, len(bits), size)]


def xor(bits, key):
    return [int(bool(bits[index]) != bool(key[index])) for index in range(len(bits))]




