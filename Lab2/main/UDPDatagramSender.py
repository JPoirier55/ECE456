
import argparse
import sys
from struct import *
from udp_utils import *
import binascii


def convert_ip_binary(ip):
    return ''.join(bin(int(x)+256)[3:] for x in reversed(ip.split('.')))

def padZeroes(hexNum):
    if len(hexNum) == 8:
        hexNum = '0000' + hexNum
    return hexNum

def tobits_inline(raw_string):
    """
    Converts a string of chars to a list of bits
    :param raw_string: incoming string to be converted
    :return: list/array of bits corresponding to incoming string
    :exception: FormatError will catch if the incoming string is
        not an instance of python basestring
    """
    if not isinstance(raw_string, basestring):
        raise FormatError('This is not a correctly formatted string')

    result = ''
    for c in raw_string:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        for b in bits:
            result += b
    return result

def split(bits, size):
    """
    Splits a list of bits into two lists of certain size
    :param bits: list of bits to be split
    :param size: size of smaller lists to be made
    :return: list of lists of bits
    """
    return [bits[i:i+size] for i in xrange(0, len(bits), size)]

def compute_checksum(data):
    sum_bits = '0'
    for bits in split(data, 16):
        sum_bits = bin(int(bits, 2) + int(sum_bits, 2))

        if len(bin(int(sum_bits, 2))[2:]) > 16:
            sum_bits = bin(int('1', 2) + int(sum_bits[2:], 2))
            sum_bits = sum_bits[3:]

    checksum = int(sum_bits, 2) ^ 0xFFFF

    return checksum



def main():
    """
    Main access point for running from terminal commands
    Can use python encrypt.py -h for help with commands
    :return: none
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile', help='use --inputfile <filename>', required=True)
    parser.add_argument('--sourceIP', help='use --sourceIP <sourceIP>', required=True)
    parser.add_argument('--destinationIP', help='use --destinationIP <destinationIP>', required=True)
    parser.add_argument('--sourcePort', help='use --sourcePort <sourcePort>', required=True)
    parser.add_argument('--destinationPort', help='use --destinationPort <destinationPort>', required=True)
    parser.add_argument('--datagramFilename', help='use --datagramFilename <datagramFilename>', required=True)


    args = parser.parse_args()


    dest_ip = args.destinationIP
    source_ip = args.sourceIP
    source_port = args.sourcePort
    dest_port = args.destinationPort
    datagram_filename = args.datagramFilename
    datagram_file = read_file(args.inputfile)

    dest_ip_bin = convert_ip_binary(dest_ip)
    source_ip_bin = convert_ip_binary(source_ip)

    datagram = ''
    print datagram

    data = tobits_inline(datagram_file)
    datagram += source_ip_bin
    print datagram
    datagram += dest_ip_bin
    print datagram
    datagram += '00000000'
    print 'add zeroes', datagram
    datagram += "{0:#0{1}b}".format(17, 18)[2:]
    print datagram
    datagram += tobits_inline(str(len(split(data, 16)) + 8))
    print datagram
    datagram += tobits_inline(source_port)
    print datagram
    datagram += tobits_inline(dest_port)
    print datagram
    # print "{0:#0{1}b}".format(len(split(data, 16)), 10)
    datagram += "{0:#0{1}b}".format(len(split(data, 16)), 10)[2:]

    print datagram
    datagram += '0000000000000000'
    print datagram
    # print data
    datagram += data
    # print datagram
    checksum = compute_checksum(datagram)
    # print checksum
    checksum = "{0:#0{1}b}".format(checksum, 18)[2:]
    print datagram
    print checksum
    datagram = datagram[:144] + checksum + datagram[160:]
    print datagram
    print checksum
    # print "{0:#0{1}x}".format(checksum, 6)[2:]

    with open(datagram_filename, 'wb+') as f:
        f.write(datagram)
if __name__ == '__main__':
    sys.exit(main())