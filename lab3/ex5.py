import csv
import string
import random as r
import time as t
import hashlib as h
from ex2 import *

def read_hash_file(filein):
    hash_list = []
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        for l in fin.readlines():
            if len(l) == 34:
                hash_list.append(l.strip())
    return hash_list

def parse_data_to_csv(data):
    with open('ex5.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(data)

if __name__ == "__main__":
    time_start = t.perf_counter()
        
    rand_str_dict = dict()
    hash_list = read_hash_file('hashes.txt')
    length = len(hash_list)
    
    i = 1
    while len(hash_list) > 0:
        for _ in range(pow(94, i)):
            rand_str = str_generator(size=i, chars=string.ascii_lowercase + string.digits + ' ' + string.punctuation)
            rand_hash = gen_hash(rand_str)
            if rand_hash in hash_list:
                rand_str_dict[rand_hash] = rand_str
                print(f"{rand_str} is {rand_hash}")
                hash_list.remove(rand_hash)
                print('Remaining length: ', len(hash_list))
                parse_data_to_csv([rand_hash, rand_str])
        i += 1
        
    time_taken = t.perf_counter() - time_start
    print(f"Total time taken(s): {time_taken}")
    print(f"Average time taken(s): {time_taken / length}")

    write_file('ex2_hash.txt', str_list_output)

    print(t.perf_counter() - time_start)
