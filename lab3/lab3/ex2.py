import string
import time as t
import hashlib as h

str_list_output = hash_list = []
characters = string.ascii_lowercase + string.digits

# Current guess from generate() function
current_guess = ""

# Indexes for each character)
digits = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

def read_file(filein):
    with open(filein, mode="r", encoding="utf-8", newline="\n", errors="ignore") as fin:
        return [l.strip() for l in fin.readlines()]

def write_file(fileout, str_list_output):
    fout = open(fileout, mode="w", encoding="utf-8", newline="\n") 
    fout.write('\n'.join(str_list_output))
    fout.close()

def gen_hash(string):
    return h.md5(string.encode()).hexdigest()

def check_hash_collision(rand_str):
    global str_list_output, hash_list
    rand_hash = gen_hash(str(rand_str))
    if rand_hash in hash_list:
        rand_str_dict[rand_hash] = rand_str
        str_list_output.append(rand_str)
        print(f"{rand_str} is {rand_hash}")
        hash_list.remove(rand_hash)
        print('Remaining length: ', len(hash_list))

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
    hash_list = read_file('hash5.txt')
    length = len(hash_list)

    while len(hash_list) > 0:
        generate_brute_force(5)

    time_taken = t.perf_counter() - time_start
    print(f"Total time taken(s): {time_taken}")
    print(f"Average time taken(s): {time_taken / length}")

    write_file('ex2_hash.txt', str_list_output)
