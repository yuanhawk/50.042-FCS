#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

from present import *
import argparse

nokeybits = 80
blocksize = 64


def is_empty(inp, s):
    if s is None:
        print(f'{inp} is empty')
    else:
        if inp == 'infile':
            with open(s, mode="rb") as fin:
                with open('Tux_enc.pbm', mode='wb'):
                    for l in fin.readlines():
                        for b in l:
                            print(b)



def ecb(infile, outfile, key, mode):
    pass



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

    is_empty('infile', infile)
    is_empty('outfile', outfile)
    is_empty('keyfile', keyfile)
    is_empty('mode', mode)
