#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Done by: Tan Li Yuan 1004326
# Simple file read in/out


# Import libraries
import os
import sys
import argparse
import string

def doStuff(filein, fileout, key, mode):
    key_state = checkKey(key)
    mode_state = checkMode(mode)
    if (key_state == False or mode_state != None):
        pass

    fin = None
    file_name, file_ext = os.path.splitext(filein)
    fout_b = open(fileout, mode="wb")  # binary write mode
    if file_ext == '' or file_ext == '.bin':
        with open(filein, mode="rb") as fin:
            new_text = renderString(fin, mode_state, None)
            fout_b.write(new_text)
    else:
        with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
            new_text = renderString(fin, mode_state, 'utf-8')
            fout_b.write(new_text)
    fout_b.close()
            # file will be closed automatically when interpreter reaches end of the block

def renderString(fin, mode_state, enc):
    text = fin.read(1)
    # do stuff
    new_text = bytearray()
    while text:
        if mode_state == '-':
            new_text.append((ord(text) - int(key)) % 256)
        elif mode_state == '+':
            new_text.append((ord(text) + int(key)) % 256)
        text = fin.read(1)

    return new_text


def checkKey(key):
    if (int(key) < 0 or int(key) > 255):
        print('Error invalid key')
        return False
    return True

def checkMode(mode):
    mode_state = None
    if mode == 'd' or mode == 'D':
        mode_state = '-'
    elif mode == 'e' or mode == 'E':
        mode_state = '+'
    else:
        print('Error invalid mode')
    return mode_state


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")
    parser.add_argument("-k", dest="key", help="key")
    parser.add_argument("-m", dest="mode", help="mode")

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.key
    mode = args.mode
    
    doStuff(filein, fileout, key, mode)

    # all done
