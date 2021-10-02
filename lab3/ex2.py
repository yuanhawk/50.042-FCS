import string
import random as r
import time as t
import hashlib as h

def read_hash_file(filein):
    hash_list = []
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        return [l.strip() for l in fin.readlines()]

def write_file(fileout, str_list_output):
    fout = open(fileout, mode="w", encoding="utf-8", newline="\n") 
    fout.write('\n'.join(str_list_output))
    fout.close()

def gen_hash(string):
    return h.md5(string.encode()).hexdigest()

def str_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(r.choice(chars) for _ in range(size))

def rev_hash_output(filein, fileout):
    time_start = t.perf_counter()

    rand_str_dict = dict()
    hash_list = read_hash_file(filein)
    length = len(hash_list)

    str_list_output = []
    while len(hash_list) > 0:
        rand_str = str_generator()
        rand_hash = gen_hash(rand_str)
        if rand_hash in hash_list:
            rand_str_dict[rand_hash] = rand_str
            print(f"{rand_str} is {rand_hash}")
            str_list_output.append(rand_str)
            hash_list.remove(rand_hash)
            print(str_list_output)
            print('Remaining length: ', len(hash_list))

    time_taken = t.perf_counter() - time_start
    print(f"Total time taken(s): {time_taken}")
    print(f"Average time taken(s): {time_taken / length}")

    write_file(fileout, str_list_output)

    print(t.perf_counter() - time_start)


if __name__ == "__main__":
    rev_hash_output('hash5.txt', 'ex2_hash.txt')
    pass

    time_start = t.perf_counter()

    rand_str_dict = dict()
    hash_list = read_hash_file('hash5.txt')
    length = len(hash_list)

    str_list_output = []
    while len(hash_list) > 0:
        rand_str = str_generator()
        rand_hash = gen_hash(rand_str)
        if rand_hash in hash_list:
            rand_str_dict[rand_hash] = rand_str
            print(f"{rand_str} is {rand_hash}")
            str_list_output.append(rand_str)
            hash_list.remove(rand_hash)
            print(str_list_output)
            print('Remaining length: ', len(hash_list))

    time_taken = t.perf_counter() - time_start
    print(f"Total time taken(s): {time_taken}")
    print(f"Average time taken(s): {time_taken / length}")

    write_file('ex2_hash.txt', str_list_output)

    print(t.perf_counter() - time_start)
