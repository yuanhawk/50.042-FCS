# * Name of Student(s): Tan Li Yuan, Teo Yew Xuan
# * Student ID(s): 1004326, 1004452

import time as t

from dhke import *
from babygiant import *

i = 4

if __name__ == "__main__":
    while True:
        start = t.time()
        print(f'Attempting to break {2**i} bits')
        with open('attack.txt', 'a') as fout:
            p, alpha = dhke_setup(2**i)
            # print("Generate P and alpha:")
            # print("P:", p)
            # print("alpha:", alpha)
            # print()
            a = gen_priv_key(p)
            b = gen_priv_key(p)
            # print("My private key is: ", a)
            # print("Test other private key is: ", b)
            # print()
            A = get_pub_key(alpha, a, p)
            B = get_pub_key(alpha, b, p)
            # print("My public key is: ", A)
            # print("Test other public key is: ", B)
            # print()
            sharedkey = get_shared_key(B, a, p)
            # print("My shared key is: ", sharedkey)
            # a = baby_giant(alpha, A, p)
            # b = baby_giant(alpha, B, p)
            guesskey1 = primes.square_multiply(A, b, p)
            guesskey2 = primes.square_multiply(B, a, p)
            # print("Guess key 1:", guesskey1)
            # print("Guess key 2:", guesskey2)
            # print("Actual shared key :", sharedkey)
            if guesskey1 == sharedkey or guesskey2 == sharedkey:
                print(f'Finished breaking {2**i} bits in {t.time() - start} sec')
                fout.write(f'Finished breaking {2**i} bits in {t.time() - start} sec')
            else:
                print('Incorrect guess')
                break
            fout.close()
        i += 1