import string
import random as r
import time as t
import hashlib as h
from ex2 import *

def read_salt_hash_file(filein):
    hash_list = []
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        for l in fin.readlines():
            strs = l.strip() + str_generator(size=1, chars=string.ascii_lowercase)
            hash_list.append(gen_hash(strs))
        write_file('salted6.txt', hash_list)

if __name__ == "__main__":
    read_salt_hash_file('ex2_hash.txt')
