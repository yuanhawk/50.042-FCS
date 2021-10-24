# 50.042 FCS Lab 6 template
# Year 2021

from prime import *
import random as r


def dhke_setup(nb):
    #largest prime
    # p = 1208925819614629174706189
    # alpha = p - 2

    num = '0b'
    for i in range(nb):
        num += f'{r.randint(0, 1)}'
    p = 941
    alpha = 627

    # a, b = gen_priv_key(p)
    # a_pub = get_pub_key(alpha, a, p)
    # b_pub = get_pub_key(alpha, b, p)
    #
    # k_ab = get_shared_key(b_pub, a, p)
    # k_ba = get_shared_key(a_pub, b, p)

    # print (str(k_ab), str(k_ba))

    pass


def gen_priv_key(p):
    return r.randrange(2, p-2), r.randrange(2, p-2)

def get_pub_key(alpha, a, p):
    return square_multiply(alpha, a, p)


def get_shared_key(keypub, keypriv, p):
    return square_multiply(keypub, keypriv, p)


if __name__ == "__main__":
    p, alpha = dhke_setup(80)
    print("Generate P and alpha:")
    print("P:", p)
    print("alpha:", alpha)
    print()
    a = gen_priv_key(p)
    b = gen_priv_key(p)
    print("My private key is: ", a)
    print("Test other private key is: ", b)
    print()
    A = get_pub_key(alpha, a, p)
    B = get_pub_key(alpha, b, p)
    print("My public key is: ", A)
    print("Test other public key is: ", B)
    print()
    sharedKeyA = get_shared_key(B, a, p)
    sharedKeyB = get_shared_key(A, b, p)
    print("My shared key is: ", sharedKeyA)
    print("Test other shared key is: ", sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())
