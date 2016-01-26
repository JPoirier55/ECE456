
from cipher_utils import *

KEY = [1, 1, 1, 1, 1, 1, 1, 1]
SPACE = [0, 0, 1, 0, 0, 0, 0, 0]


def decrypt(raw_data):
    decrypted_bits = []
    byte_list = []
    bits = tobits(raw_data)
    blocks = split(bits, 16)

    for block in blocks:
        block_16 = BlockObject(block)

        if len(block_16.bit_string) == 16:
            split_bits = split(block_16.bit_string, 8)
            xor_bits = xor(split_bits[1], KEY)
            new_bytes = xor_bits + split_bits[0]
            byte_list.append(new_bytes)

        elif len(block_16.bit_string) == 8:
            block_8 = BlockObject(block_16.bit_string)
            xor_bits = xor(block_8.bit_string, KEY)
            new_bytes = xor_bits + SPACE
            byte_list.append(new_bytes)
        else:
            raise FormatError('There is an incorrect number of bits in packet #{0} '
                              'of object:{1} '.format(block_16.bit_string, block_16))
    for bytes in byte_list:
        decrypted_bits += bytes

    return decrypted_bits

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile', help='use --inputfile <filename>', required=True)
    parser.add_argument('--outputfile', help='use --outputfile <filename>', required=True)

    args = parser.parse_args()

    input_message = read_file(args.inputfile)
    bits_encrypted = decrypt(input_message)
    text_encrypted = frombits(bits_encrypted)
    write_file(args.outputfile, text_encrypted)

if __name__ == '__main__':
    sys.exit(main())