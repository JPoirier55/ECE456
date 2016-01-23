
class BlockObject:

    def __init__(self, bit_string):
        """
        :param char_string: incoming string to be converted into bits
        :return: sets self.string and self.bit_string accordingly
        """
        self.bit_string = bit_string

def read_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data



def tobits(string):
    result = []
    for c in string:
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
    blocks = [bits[i:i+size] for i in xrange(0, len(bits), size)]
    return blocks


def xor(bits, key):
    return [int(bool(bits[index]) != bool(key[index])) for index in bits]


if __name__ == '__main__':
    p = read_file('input.txt')
    print p
    s = 'jakedf'
    final_bits = []
    byte_list = []
    bits = tobits(p)
    blocks = split(bits, 16)
    for block in blocks:
        block_16 = BlockObject(block)
        print 'Initial 16 bits', block_16.bit_string
        if len(block_16.bit_string) == 16:
            block_8_1 = BlockObject(split(block_16.bit_string, 8)[0])
            block_8_2 = BlockObject(split(block_16.bit_string, 8)[1])
            new_block_16 = BlockObject(block_8_2.bit_string + block_8_1.bit_string)
            split_bits = split(new_block_16.bit_string, 8)
            key = [1, 1, 1, 1, 1, 1, 1, 1]
            xor_bits = xor(split_bits[1], key)
            print xor_bits
            split_bits = split_bits[0] + xor_bits
            print split_bits
            byte_list.append(split_bits)
    print byte_list

    for byte in byte_list:
        final_bits += byte
    print final_bits
    print frombits(final_bits)



    ob = BlockObject(s)
    # print ob.bit_string


    # ob1 = BlockObject(split(ob.bit_string, )
    # ob = BlockObject(s)
    # print ob.string
    # print ob.bit_string
    # t = split(ob.bit_string, 16)
    # print t
