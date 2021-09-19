#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Done by: Tan Li Yuan 1004326
# Simple file read in/out


# Import libraries
import sys
import argparse
import string

def doStuff(filein, fileout, key, mode):
    key_state = checkKey(key)
    mode_state = checkMode(mode)
    if (key_state == False or mode_state == None):
        pass

    fout = open(fileout, mode="w", encoding="utf-8", newline="\n")  # write mode

    # PROTIP: pythonic way
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        text = fin.read()
        # print(text)
        # do stuff
        new_text = ''
        if mode_state == '-':
            for t in text:
                new_text += chr((ord(t) - int(key)) % 256)
        elif mode_state == '+':
            for t in text:
                new_text += chr((ord(t) + int(key)) % 256)

        fout.write(new_text)
        # file will be closed automatically when interpreter reaches end of the block
    # close all file streams
    fin.close()
    fout.close()

    

def checkKey(key):
    if (int(key) < 1 or int(key) > len(string.printable) - 1):
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
