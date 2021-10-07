import os
import csv
import gzip
from ex2 import *

rand_str_dict = {}

def unzip_file(filein):
    with gzip.open(filein, mode="rt", encoding="utf-8", newline="\n", errors="ignore") as fin:
        for word in fin:
            check_hash_collision(word.strip())

def read_hash_file(filein):
    global hash_list
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        for l in fin.readlines():
            if len(l) == 34 and l.strip() not in rand_str_dict.keys():
                hash_list.append(l.strip())
    print('Remaining length: ', len(hash_list))

def read_csv_to_data(filename):
    global rand_str_dict
    if not os.path.isfile(filename):
        open(filename, 'w').close()
    else:
        with open(filename, 'r') as myFile:
            csv_file = csv.reader(myFile)
            for line in csv_file:
                rand_str_dict[line[0]] = line[1]
            print(rand_str_dict)


def parse_data_to_csv(data):
    with open('ex5.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(data)

def check_hash_collision(rand_str):
    global time_taken
    rand_hash = gen_hash(str(rand_str))
    if rand_hash in hash_list:
        rand_str_dict[rand_hash] = rand_str
        print(f"{rand_str} is {rand_hash}")
        hash_list.remove(rand_hash)
        print('Remaining length: ', len(hash_list))
        print('Time taken: ', t.perf_counter() - time_start)
        time_taken = t.perf_counter()
        parse_data_to_csv([rand_hash, rand_str])

if __name__ == "__main__":
    time_start = t.perf_counter()

    rand_str_dict = dict()
    read_csv_to_data('ex5.csv')
    read_hash_file('hashes.txt')
    size = len(hash_list)

    # unzip_file('crackstation.txt.gz')

    with open('test.txt', mode="r", encoding="utf-8", newline="\n", errors='ignore') as fin:
        for l in fin.readlines():
            check_hash_collision(l.strip())

    # dir = 'db'
    # for file in os.listdir(dir):
    #     filename = os.fsdecode(file)
    #     if filename.endswith(".txt"):
    #         with open(f'{dir}/{filename}', mode="r", encoding="utf-8", newline="\n", errors='ignore') as fin:
    #             for l in fin.readlines():
    #                 check_hash_collision(l.strip())