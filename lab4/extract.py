#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

import argparse
from collections import Counter

def getInfo(headerfile):
    header = []

    with open(headerfile, 'rb') as hf:
        header = hf.read();
        header_len = len(header)
    return header, header_len


def extract(infile, outfile, headerfile):
    header, header_len = getInfo(headerfile)
    encrypted = []
    print(header, header_len)

    with open(infile, 'rb') as fin:
        fin.read(header_len)
        while True:
            byte_in = fin.read(8)
            if byte_in == b"":
                break
            else:
                encrypted.append(byte_in)
    #print(encrypted)
    block_freqency = dict(Counter(encrypted))
    print(block_freqency)

    with open(outfile, 'wb') as fout:
        fout.write(header)
        fout.write(b'\n')
        fout.close()
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
