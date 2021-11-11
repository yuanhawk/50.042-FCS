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


if __name__ == "__main__":
    rsakey_pub = get_key('mykey.pem.pub')
    rsakey_priv = get_key('mykey.pem.priv')

    # print(key)
    # public key
    # print(rsakey_pub.n)
    # print(rsakey_pub.e)
    # private key
    # print(rsakey_priv.n)
    # print(rsakey_priv.d)
    i = hash_msg('mydata.txt')

    e = square_multiply(i, rsakey_pub.e, rsakey_pub.n)
    d = square_multiply(e, rsakey_priv.d, rsakey_priv.n)
    assert (i == d)

