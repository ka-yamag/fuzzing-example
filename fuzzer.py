#! /usr/bin/env python3

import sys
import random

# read bytes from our valid JPEG and return them in a mutable bytearray
def get_bytes(filename):
    f = open(filename, "rb").read()
    return bytearray(f)


def create_new(data):
    f = open("mutated.jpg", "wb+")
    f.write(data)
    f.close()


def bit_flip(data):
    # Not count the first 2 bytes or the last 2 bytes in array
    num_of_flips = int((len(data) - 4) * .01)

    indexes = range(4, (len(data) - 4))

    chosen_indexes = []

    counter = 0
    while counter < num_of_flips:
        chosen_indexes.append(random.choice(indexes))
        counter += 1

    print("Number of indexes chosen: " + str(len(chosen_indexes)))
    print("Indexes chosen: " + str(chosen_indexes))

    for x in chosen_indexes:
        current = data[x]
        current = (bin(current).replace("0b", ""))
        # 0 padding if it's less then 8 digits
        current = "0" * (8 - len(current)) + current

        # choice picked bit in a byte
        indexes = range(0, 8)
        picked_index = random.choice(indexes)
        
        new_number = []

        for i in current:
            new_number.append(i)

        # bit flipping
        if new_number[picked_index] == "1":
            new_number[picked_index] = "0"
        else:
            new_number[picked_index] = "1"
        
        current = ''
        for i in new_number:
            current += i

        # convert that string to an integer
        current = int(current, 2)

        # change the number in our byte array to our new number we just constructed
        data[x] = current

    return data

def magic(data):
    # the first number in the tuple is the byte-size of the magic number
    # the second number is the byte value in decimal of the first byte
    magic_vals = [
            (1, 255), # 0xff
            (1, 255), # 0xff
            (1, 127), # 0x7f
            (1, 0),   # 0x00
            (2, 255), # 0xff00
            (2, 0),   # 0x0000
            (4, 255), # 0xff000000
            (4, 0),   # 0x00000000
            (4, 128), # 0x80000000
            (4, 64),  # 0x40000000
            (4, 127)  # 0x7f000000
            ]
    picked_magic = random.choice(magic_vals)

    length = len(data) - 8
    index = range(0, length)


if len(sys.argv) < 2:
    print('Usage: fuzzer.py <valid_jpg>')
else:
    filename = sys.argv[1]
    data = get_bytes(filename)
    mutated_data = bit_flip(data)
    create_new(mutated_data)
