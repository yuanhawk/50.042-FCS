# 50.042 FCS Lab 7
# Year 2021
# * Name of Student(s): Tan Li Yuan, Teo Yew Xuan
# * Student ID(s): 1004326, 1004452

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from primes import square_multiply

def get_key(fname, mode='r'):
    key = open(fname, mode)
    return RSA.importKey(key.read())

def hash_msg(fname, mode='r'):
    text = open(fname, mode)
    h = SHA256.new()
    h.update(text.read().encode())
    return int(h.hexdigest(), 16)

def encrypt(i):
    pub = get_key('mykey.pem.pub')
    # public key
    # print(pub.n)
    # print(pub.e)
    return square_multiply(i, pub.e, pub.n)

def decrypt(e):
    priv = get_key('mykey.pem.priv')
    # private key
    # print(priv.n)
    # print(priv.d)
    return square_multiply(e, priv.d, priv.n)

def check_text_is_same(i):
    e = encrypt(i)
    d = decrypt(e)
    return i == d

if __name__ == "__main__":
    if check_text_is_same(hash_msg('mydata.txt')):
        print('Hash message and decrypted hash message is the same!')
    else:
        print('Hash message and decrypted hash message is not the same!')

