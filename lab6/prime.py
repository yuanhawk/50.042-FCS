# 50.042 FCS Lab 6 template
# Year 2021

import random as r
import time as t


# y = a^x mod n
def square_multiply(a, x, n):
    y = 1
    for i in bin(x)[2:]:
        y = y * y % n
        if i == '1':
            y = y * a % n
    return y


def largest_pow_2(val):
    val_bin = [s for s in bin(val)[2:]]
    largest_ind = len(val_bin) - val_bin[::-1].index('1')
    return len(val_bin) - largest_ind, int(''.join(val_bin[:largest_ind]), 2)


# Find n - 1 = 2^k * m
# Choose a: 1 < a < n - 1
# Compute b_0 = a^m(mod n), b_i = b_{i-1}^2
# b_0 = 1 || b_0 = -1 prime (probably)
# b_i = 1 composite
# b_i = -1 prime (probably)
def miller_rabin(n, acc):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    _, m = largest_pow_2(n - 1)

    for _ in range(acc):
        # pick random a
        a = 2 + r.randint(1, n - 4)

        x = square_multiply(a, m, n)
        if x == 1 or x == n - 1:
            return True
        while m != n - 1:
            x = square_multiply(x, 2, n)
            m *= 2
            if x == 1:
                return False
            elif x == n - 1:
                return True
        return False
    return None

    # val = n - 1
    # val_bin = bin(n - 1)[2:]
    #
    # k = 0
    # for i in range(len(val_bin) - 1, -1, -1):
    #     if val_bin[i] == '1':
    #         break
    #     val >>= 1
    #     k += 1
    # print (k)

    # find odd no d s.t. n-1  is d* 2**r


def gen_prime_nbits(n):
    x = r.getrandbits(n)
    while not miller_rabin(x, 4):
        x = r.getrandbits(n)
    return x


if __name__ == "__main__":
    # print ('3^5 mod 11 = 1')
    # print (square_multiply(3, 5, 11))

    # a = 4
    # prime_num = []
    # for i in range(0, 100):
    #     if miller_rabin(i, a) is True:
    #         prime_num.append(i)
    #         t.sleep(0.5)
    #
    # print (prime_num)

    # print('Is 561 a prime?')
    # print(miller_rabin(561, 2))
    # print('Is 27 a prime?')
    # print(miller_rabin(27, 2))
    # print('Is 61 a prime?')
    # print(miller_rabin(61, 2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (80 bits):')
    print(gen_prime_nbits(80))
