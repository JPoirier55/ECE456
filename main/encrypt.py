
"""
Author: Jake Poirier
Date: 1/25/2016
Class: ECE456
Assignment: Lab 1
"""


from cipher_utils import *
import argparse

SPACE = [0, 0, 1, 0, 0, 0, 0, 0]


def encrypt(raw_data, key):
    """
    Encrypts incoming data read from a text file and writes it to a file
    :param raw_data: incoming text data
    :param key: list of bits correspond to algorithm key
    :return: text that has been encrypted
    """

    encrypted_bits = []
    byte_list = []
    bits = tobits(raw_data)
    blocks = split(bits, 16)

    for block in blocks:
        block_16 = BlockObject(block)

        if len(block_16.bit_string) == 16:
            split_bits = split(block_16.bit_string, 8)
            xor_bits = xor(split_bits[0], key)
            new_bytes = split_bits[1] + xor_bits
            byte_list.append(new_bytes)

        elif len(block_16.bit_string) == 8:
            block_8 = BlockObject(block_16.bit_string)
            xor_bits = xor(block_8.bit_string, key)
            new_bytes = SPACE + xor_bits
            byte_list.append(new_bytes)
        else:
            raise FormatError('There is an incorrect number of bits in packet #{0} '
                              'of object:{1} '.format(block_16.bit_string, block_16))
    for bytes in byte_list:
        encrypted_bits += bytes

    text_encrypted = frombits(encrypted_bits)
    return text_encrypted


def main():
    """
    Main access point for running from terminal commands
    Can use python encrypt.py -h for help with commands
    :return: none
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile', help='use --inputfile <filename>', required=True)
    parser.add_argument('--outputfile', help='use --outputfile <filename>', required=True)
    parser.add_argument('--keyfile', help='use --keyfile <filename>', required=True)

    args = parser.parse_args()

    key = read_key(args.keyfile)
    input_message = read_file(args.inputfile)
    text_encrypted = encrypt(input_message, key)
    write_file(args.outputfile, text_encrypted)

if __name__ == '__main__':
    sys.exit(main())
