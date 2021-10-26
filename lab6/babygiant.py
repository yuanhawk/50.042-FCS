# 50.042 FCS Lab 6 template
# Year 2021

import csv
import math
import primes
import pandas as pd


def baby_step(alpha, beta, p, fname):
    m = math.ceil(math.sqrt(p - 1))

    with open(fname, 'w') as fout:
        writer = csv.writer(fout)
        for j in range(0, m):
            output = (beta * alpha ** j) % p
            writer.writerow([str(output)])


def giant_step(alpha, p, fname):
    m = math.ceil(math.sqrt(p - 1))
    with open(fname, 'w') as fout:
        for g in range(0, m):
            writer = csv.writer(fout)
            output = primes.square_multiply(alpha, g * m, p)
            writer.writerow([str(output)])


def baby_giant(alpha, beta, p):
    m = math.ceil(math.sqrt(p - 1))
    baby_step(alpha, beta, p, 'baby.csv')
    giant_step(alpha, p, 'giant.csv')

    bs = pd.read_csv('baby.csv', index_col=False, header=None)[0].values.tolist()
    gs = pd.read_csv('giant.csv', index_col=False, header=None)[0].values.tolist()

    dup = set(bs).intersection(set(gs))
    print (dup)

    if len(dup) > 0:
        val = list(dup)[0]
        x_b = bs.index(val)
        x_g = gs.index(val)
        return x_g * m - x_b
    else:
        return -1


if __name__ == "__main__":
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    """
    p = 17851
    alpha = 17511
    A = 2945
    B = 11844
    sharedkey = 1671
    a = baby_giant(alpha, A, p)
    b = baby_giant(alpha, B, p)
    guesskey1 = primes.square_multiply(A, b, p)
    guesskey2 = primes.square_multiply(B, a, p)
    print("Guess key 1:", guesskey1)
    print("Guess key 2:", guesskey2)
    print("Actual shared key :", sharedkey)
