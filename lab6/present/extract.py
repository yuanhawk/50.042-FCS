#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS
# * Name of Student(s): Tan Li Yuan, Teo Yew Xuan
# * Student ID(s): 1004326, 1004452

import argparse

def getInfo(headerfile):
    with open(headerfile, 'rb') as hf:
        header = hf.read()
        header_len = len(header)
    return header, header_len


def extract(infile, outfile, headerfile):
    header, header_len = getInfo(headerfile)
    encrypted = []
    print(header, header_len)

    frequency = -1
    block_frequency = {}
    with open(infile, 'rb') as fin:
        fin.read(header_len)
        while byte_in := fin.read(8):
            if byte_in != b"":
                encrypted.append(byte_in)
                if byte_in not in block_frequency.keys():
                    block_frequency[byte_in] = 1
                else:
                    block_frequency[byte_in] += 1
                    if block_frequency[byte_in] > frequency:
                        frequency = block_frequency[byte_in]
                        most_freq_block = byte_in

        decrypted = []
        for e in encrypted:
            bin = b'0' * 8 if e == most_freq_block else b'1' * 8
            decrypted.append(bin.decode())

        decrypted = ''.join(decrypted).encode()

    with open(outfile, 'wb') as fout:
        fout.write(header)
        fout.write(b'\n')
        fout.write(decrypted)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile', help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile', help='output PBM file')
    parser.add_argument('-hh', dest='headerfile', help='known header file')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    headerfile = args.headerfile

    print('Reading from: %s' % infile)
    print('Reading header file from: %s' % headerfile)
    print('Writing to: %s' % outfile)

    success = extract(infile, outfile, headerfile)
