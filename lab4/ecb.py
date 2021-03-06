#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS
# * Name of Student(s): Tan Li Yuan, Teo Yew Xuan
# * Student ID(s): 1004326, 1004452

import argparse
import math

from present import *

nokeybits = 80
blocksize = 64

def pad(block):
    elen = len(block) % blocksize
    if elen:
        block += bytes(blocksize - elen)
    return block

def unpad(s):
    return s.decode('ascii').strip().strip('\x00')

def get_bin_from_bytes(bytes):
    block_binary = ''
    for byte in bytes:
        block_binary += pad_binary(byte, 8)
    return block_binary

def get_bytes_from_bin(binary):
    result = int(binary).to_bytes(8, byteorder='big')
    return result
    # return binary.

def read_input(filein, fileout, filekey, mode):

    with open(filekey, mode='r') as fin:
        key = get_hex_int(fin.read())

    with open(filein, mode="rb") as fin:
        with open(fileout, mode='wb') as fout:
            fin_hex = fin.read()
            encrypted_byte = b''

            if mode == 'e':

                for i in range(math.ceil(len(fin_hex) / 8)):
                    block = fin_hex[i * 8:(i + 1)*8]
                    if len(block) < 8:
                        block = block.ljust(8, b'0')
                    block_bin_str = get_bin_from_bytes(block)
                    block_bin_int = get_bin_int(block_bin_str)
                    encrypted_block = present(block_bin_int, key)
                    block_byte = get_bytes_from_bin(encrypted_block)

                    encrypted_byte += block_byte

            if mode == 'd':
                for i in range(math.ceil(len(fin_hex) / 8)):
                    block = fin_hex[i * 8:(i + 1)*8]
                    block_bin_str = get_bin_from_bytes(block)
                    block_bin_int = get_bin_int(block_bin_str)
                    encrypted_block = present_inv(block_bin_int, key)
                    block_byte = get_bytes_from_bin(encrypted_block)

                    #reference to last block which is padded
                    if i == len(fin_hex) // 8 - 1:
                        block_byte = block_byte.rstrip(b'0')
                    encrypted_byte += block_byte


            fout.write(encrypted_byte)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile', help='input file')
    parser.add_argument('-o', dest='outfile', help='output file')
    parser.add_argument('-k', dest='keyfile', help='key file')
    parser.add_argument('-m', dest='mode', help='mode')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    keyfile = args.keyfile
    mode = args.mode

    read_input(infile, outfile, keyfile, mode)
