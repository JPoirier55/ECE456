
"""
Author: Jake Poirier
Date: 1/25/2016
Class: ECE456
Assignment: Lab 1
"""

import sys


class BlockObject:
    """
    Object class for blocks of 16 bit packets
    """
    def __init__(self, bit_string):
        """
        :param bit_string: incoming string to be converted into bits
        :return: sets self.bit_string to the incoming bit_string
        """
        self.bit_string = bit_string


class FormatError(Exception):
    """
    Base class for exceptions in this module
    """
    pass


def read_key(filename):
    """
    Parses the data from a key file and puts it into correct format
    :param filename: filename of the key for encryption
    :return: list of bits corresponding to key
    """
    key_raw = read_file(filename)
    key_raw = key_raw.split(',')
    key = []
    for bit in key_raw:
        key.append(int(bit))
    return key


def read_file(filename):
    """
    Reads a file to be encrypted
    :param filename: filename to be encrypted
    :return: the data as an object
    :exception: IOError will catch whether or not there was an input error
    """
    data = None
    try:
        with open(filename, 'r') as file_read:
            data = file_read.read()
    except IOError, e:
        sys.stderr('File {0} has occured an error:'.format(filename, e))
    return data


def write_file(filename, data):
    """
    Writes the encrypted data to a file
    :param filename: filename chosen to be created or rewritten with encrypted data
    :param data: incoming data that has been encrypted
    :return: none
    :exception: IOError will catch whether or not there was an output error
    """
    try:
        with open(filename, 'w') as file_write:
            file_write.write(data)
    except IOError, e:
        sys.stderr('File {0} has occured an error:'.format(filename, e))


def tobits(raw_string):
    """
    Converts a string of chars to a list of bits
    :param raw_string: incoming string to be converted
    :return: list/array of bits corresponding to incoming string
    :exception: FormatError will catch if the incoming string is
        not an instance of python basestring
    """
    if not isinstance(raw_string, basestring):
        raise FormatError('This is not a correctly formatted string')

    result = []
    for c in raw_string:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def frombits(bits):
    """
    Converts a list of bits into a string of chars
    :param bits: array/list of bits to be converted
    :return: string of chars
    """
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def split(bits, size):
    """
    Splits a list of bits into two lists of certain size
    :param bits: list of bits to be split
    :param size: size of smaller lists to be made
    :return: list of lists of bits
    """
    return [bits[i:i+size] for i in xrange(0, len(bits), size)]


def xor(bits, key):
    """
    Performs an XOR between two lists
    :param bits: first list that is xored
    :param key: the key corresponding to the encryption algorithm
    :return: list of bits that are XOR of the incoming bits list
    """
    return [int(bool(bits[index]) != bool(key[index])) for index in range(len(bits))]

if __name__ == "__main__":
    read_key('key.txt')
