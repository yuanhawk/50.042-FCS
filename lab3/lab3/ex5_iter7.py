import csv
import json
import os
import string
import random as r
import time as t
import hashlib as h
from ex2 import *

time_start = None
# Current guess from generate() function
current_guess = ""

hash_list = []

characters = string.ascii_letters + string.digits + '-'

# Indexes for each character)
digits = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}


def read_json():
    with open("words.txt") as word_holder:
        return json.load(word_holder)[0]


def read_hash_file(filein):
    global hash_list
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        for l in fin.readlines():
            if len(l) == 34:
                hash_list.append(l.strip())

def read_csv_to_data(filename):
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


# Create a brute-force password guess using the values from digits array
def generate_brute_force(length):
    global current_guess, digits
    # Number of characters filled so far
    char_count = 0
    # Characters filled so far
    current_guess = ""
    # The current index in the digits array
    index_counter = length

    # Create the guess according to current digits array
    while char_count < length:
        char_count += 1
        current_guess += characters[digits[char_count]]
    check_hash_collision(current_guess)

    # Incerement the relative key in the index array for next run
    digits_modded = False
    while not digits_modded:
        # Increment end index value if not equal to length of character array
        if digits[index_counter] < (len(characters) - 1):
            digits[index_counter] += 1
            digits_modded = True

        # Otherwise move focus left if not already on first index in digits array
        else:
            if index_counter > 1:
                # Reset value fo existing index
                digits[index_counter] = 0
                # Move index left
                index_counter -= 1
                # Increment the value for the new index
                if digits[index_counter] < (len(characters) - 1):
                    digits[index_counter] += 1
                    digits_modded = True
            else:
                # All combinations tried. Increase password length
                #  and reset counters
                length += 1
                for pos in digits:
                    digits[pos] = 0
                digits_modded = True

if __name__ == "__main__":
    time_start = t.perf_counter()

    rand_str_dict = dict()
    read_csv_to_data('ex5.csv')
    read_hash_file('hashes.txt')
    size = len(hash_list)

    i = 7
    print(f'Brute forcing length: {i}')
    for _ in range(pow(len(characters), i)):
        generate_brute_force(i)
    print(f'Completed brute force: {i}')
