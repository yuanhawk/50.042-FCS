#/bin/bash

# Brute-force and dictionary password analyzer
# By Anthony Hartup. From the fifth article in the Python Password Analyzer series:
# https://anthscomputercave.com/tutorials/code/python_password_cracker_dictionary.html

# Dictionary mode uses the word list created with the word_grabber.py script in:
# https://anthscomputercave.com/tutorials/code/python_password_cracker_word_list.html

import random
import time
import json

# Choose which characters to use in password guesses, or use dictionary
mode = "string_full" 

#### Character lists to create passwords based on mode ####
# Upper and lower case letters with numbers
if mode == "string_full":
    characters = ["s", "a", "t", "c", "b", "d", "e", "f", "w", "g", "h", "i", \
                  "l", "p", "r", "m", "u", "n", "o", "j", "k", "x", "v", "y", \
                  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "q", "z", \
                  "S", "A", "T", "C", "B", "D", "E", "F", "W", "G", "H", "I", \
                  "L", "P", "R", "M", "U", "N", "O", "J", "K", "X", "V", "Y", \
                  "Q", "Z"]
# Lower case letters with numbers
elif mode == "string_lower":
    characters = ["s", "a", "t", "c", "b", "d", "e", "f", "w", "g", "h", "i", \
                  "l", "p", "r", "m", "u", "n", "o", "j", "k", "x", "v", "y", \
                  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "q", "z"]
# Numeric characters only for PIN-type passwords    
elif mode == "numeric":
    characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

elif mode == "dictionary": # Single run only, no bulk passwords
    # Try words starting with each letter in this order. These are all sections in the word list
    word_order = ["common", "s", "a", "t", "c", "b", "d", "e", "f", "w", "g", "h", "i", \
                  "l", "p", "r", "m", "u", "n", "o", "j", "k", "x", "v", "y", "q", "z"]
    
    # Load the word file into words_list array
    with open("words.txt") as word_holder:
        words_list = json.load(word_holder)[0]
        print(len(words_list))
        
    # Currently trying words starting with this letter in word list    
    current_letter = word_order[0]
    # Index of current word withing its letter's section
    current_letter_index = 0

# Number of guesses for current password
guesses = 0
# Current guess from generate() function
current_guess = ""
# Number of guesses for all passwords
all_guesses = 0
# Number of passwords to crack (bulk password runs only work with brute force, not dictionary)
reps = [0, 1]
# Flag to stop guessing when attempt is sucessfull
status = "ongoing"

# Length to start guessing, will increment as all combinations are tried
password_length_to_start = 1
# Current guessing length
password_length = password_length_to_start
# Length of target passwords to create for bulk runs
password_length_to_generate = 3

# String to hold the target password
target_password = ""

# Indexes for each character in a password
digits = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}


# Create a brute-force password guess using the values from digits array
def generate_brute_force():
    global target_password, current_guess, password_length, digits, status
    
    # Number of characters filled so far
    char_count = 0
    # Characters filled so far
    current_guess = ""
    # The current index in the digits array
    index_counter = password_length
    
    # Create the guess according to current digits array    
    while char_count < password_length:
        char_count += 1
        current_guess += characters[digits[char_count]]

    # Incerement the relative key in the index array for next run
    digits_modded = "no"
    while digits_modded != "yes":
        # Increment end index value if not equal to length of character array
        if digits[index_counter] < (len(characters) - 1):
            digits[index_counter] += 1
            digits_modded = "yes"

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
                    digits_modded = "yes"
            else:
                # All combinations tried. Increase password length
                #  and reset counters
                password_length += 1
                for pos in digits:
                    digits[pos] = 0                  
                digits_modded = "yes"
                print(status + ": " + current_guess)

                
# Select a password guess from the word list
def generate_dictionary_word():
    global target_password, current_guess, status, current_letter, current_letter_index, guesses, all_guesses
    # Retrieve current word from word list array
    if len(words_list[current_letter]) > 0:
        current_guess = words_list[current_letter][current_letter_index]
    # Prepare for next guess
    # Move to next index in the current letter array if not at end
    if current_letter_index < (len(words_list[current_letter]) - 1):
        current_letter_index += 1

    # If all words from that letter were tried    
    else:
        # Change to the next letter if any remaining
        if word_order.index(current_letter) < (len(word_order) - 1):
            current_letter = word_order[word_order.index(current_letter) + 1]
            # Start from beginning of new letter section
            current_letter_index = 0
            print(current_letter)
            
        else:
            #All words from all letters tried, bad luck
            status = "not_found"
            print("DONE: " + current_letter)
            all_guesses += (guesses + 1)
            guesses = 0

### MAIN LOOP
# Get the starting time to compare to end time for bulk runs  
total_time = 0.0

# Until the quota of passwords have been cracked (Bulk runs)
## or the user enters an empty password (single runs)
while reps[0] < reps[1]:
    status = "ongoing"

    
    if mode == "dictionary":
        # Reset the indexes for the all_words array to zero
        current_letter = word_order[0]
        current_letter_index = 0
    else:
        # Reset the digits array indexes to zero
        for pos in digits:
            digits[pos] = 0
        password_length = password_length_to_start
    # If multiple runs, create random target_password for this run
    if reps[1] > 1:
        # Create a string from randomly chosen characters
        target_password = ""
        while len(target_password) < password_length_to_generate:
            # Append a random index from the characters list to target password
            target_password += random.choice(characters)
        reps[0] += 1
        
    # For single runs, prompt for target password each time instead
    else:
        target_password = str(input("Enter a password to test\n"))
        
        # Leaving empty will exit main loop
        if target_password == "":
            reps[0] += 1
            status = "stopped"
            print(status)

    # Get the starting time for this run  
    this_time = time.time()
    guesses = 0
    # Start guessing until correct
    while status == "ongoing":
        # Generate a new guess
        guesses += 1
        if mode == "dictionary":
            generate_dictionary_word()
        else:
            generate_brute_force()
        if current_guess == target_password:
            elapsed = time.time() - this_time
            status = "Cracked"
            print(status + ": " + current_guess)
            print(str(guesses) + " guesses, " + str(elapsed) + " seconds.\n___________\n")
            all_guesses += guesses
            total_time += elapsed


# Calculate and display overall stats for bulk runs
if reps[1] > 1:
    print(str(all_guesses / reps[1]) + " guesses per password")
    print(str(total_time / reps[1]) + " seconds per password")
    print(str(all_guesses / float(total_time)) + " guesses per second")

### MAIN LOOP
### Get the starting time to compare to end time    
##start_time = time.time()
##
##
##
##
##
### Until the quota of passwords have been cracked
##while reps[0] < reps[1]:
##    status = "ongoing"
##
##    # Brute-force
##    if mode != "dictionary":
##        # Reset the digits array to default
##        for pos in digits:
##            digits[pos] = 0
##
##        # If multiple runs, create random target_password for this run      
##        if reps[1] != 1:
##            # Generate target password to guess
##            target_password = ""
##            # Reset current password length to default starting length
##            password_length = password_length_to_start
##            # Number of characters generated so far
##            chars = 0
##            # Create a string from randomly chosen characters
##            while chars < password_length_to_generate:
##                # Append a random index from the characters list to target password
##                target_password += random.choice(characters)
##                chars += 1
##                
##    # Dictionary, single run, program has already prompted for target password    
##    else:
##        print(current_letter)
##        current_letter = word_order[0]
##        current_letter_index = 0
##            
##    # Start guessing
##    while status == "ongoing":
##        # Generate next password guess
##        if mode != "dictionary":
##            generate_brute_force() 
##        else:
##            generate_dictionary_word()
##        if target_password == current_guess:
##            status = "Cracked"
##            print(status + ": " + current_guess + " in " + str(guesses + 1) + " guesses")
##            all_guesses += (guesses + 1)
##            guesses = 0
##        else:
##            guesses += 1
##    if status != "Cracked":
##        print(status)
##        print(str(all_guesses / reps[1]) + " guesses")
##    reps[0] += 1
##
### Calculate and display stats     
##average_time = (time.time() - start_time) / reps[1]
##print("Mode: " + mode)
##if reps[1] != 1:
##    print(str(all_guesses / reps[1]) + " guesses per password")
##    print(str(average_time) + " seconds per password")
##else:
##    print(str(average_time) + " seconds")
##
