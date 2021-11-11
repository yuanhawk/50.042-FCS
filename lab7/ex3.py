from ex2 import *
from primes import square_multiply

i = 100

# Encrypt an integer (e.g. 100) using the public key from previous part, e.g. y
# Choose a multiplier s equal to 2 and calculate: ys ≡ se mod n
# Multiply the two numbers: m ≡ y × ys mod n
# Decrypt using the private key from the previous part.

if __name__ == "__main__":
    print('Part II-------------')
    print('Encrypting: ', i)
    y = encrypt(i)
    print('Result:\n', y)
    pub = get_key('mykey.pem.pub') #part 2 public key
    ys = square_multiply(2, pub.e, pub.n)
    m = (y * ys) % pub.n
    print('Modified to:\n', m)
    d = decrypt(m)

    print('Decrypted: ', d)

