
import argparse
import sys
from struct import *
from udp_utils import *
import binascii


def convert_ip_hex(ip):
    return ''.join(hex(int(x)+256)[3:] for x in reversed(ip.split('.')))

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

def tohex_inline(raw_string):
    result = ''
    for c in raw_string:
        bits = hex(ord(c))[2:]
        bits = '00'[len(bits):] + bits
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
    bits_data = bin(int(data, 16))[2:].zfill(8)
    sum_bits = '0'
    for bits in split(bits_data, 16):
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

    pseudo_header = ''
    datagram = ''
    print datagram

    print len(datagram_file)

    pseudo_header += convert_ip_hex(source_ip)
    print 'Source IP:      ', datagram
    pseudo_header += convert_ip_hex(dest_ip)
    print "Destination IP: ", datagram
    pseudo_header += '00'
    print 'Add zeroes:     ', datagram
    pseudo_header += "{0:#0{1}x}".format(17, 4)[2:]
    print 'Add protocol 17:', datagram
    pseudo_header += "{0:#0{1}x}".format(len(datagram_file) + 8, 6)[2:]
    print 'Total length:   ', datagram
    print pseudo_header
    # datagram += pseudo_header
    print datagram
    datagram += "{0:#0{1}x}".format(int(source_port), 6)[2:]
    print 'Source port:    ', datagram
    datagram += "{0:#0{1}x}".format(int(dest_port), 6)[2:]
    print 'Desti. port:    ', datagram
    datagram += "{0:#0{1}x}".format(len(datagram_file) + 8, 6)[2:]
    print 'Total len:      ', datagram
    datagram += '0000'
    # print data
    datagram += tohex_inline(datagram_file)
    # print 'Adding data:    ', datagram
    checksum = compute_checksum(datagram)
    # datagram += hex(checksum)

    print hex(checksum)

    # checksum = "{0:#0{1}b}".format(checksum, 18)[2:]
    print datagram
    # print checksum
    # datagram = datagram[:18] + hex(checksum)[2:] + datagram[22:]
    print datagram
    datag =  bin(int(datagram, 16))[2:].zfill(8)
    # print datagram
    # print checksum
    # print "{0:#0{1}x}".format(checksum, 6)[2:]

    # datagram = split(datagram, 8)
    # print datagram
    # bytedatagram = ''
    # for byte in datagram:
    #      bytedatagram += "{0:#0{1}x}".format(int(byte, 2), 4)[2:]
    #
    # datagram_filename.write(bytedata)
    # datagram = binascii.hexlify(datagram)
    # print datagram
    with open("datagram.bin", 'wb') as f:
        f.write(datag)
    # print checksum
    import mimetypes
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

    print is_binary_string(open('datagram.bin', 'rb').read())


    print mimetypes.guess_type("datagram.bin")
if __name__ == '__main__':
    sys.exit(main())