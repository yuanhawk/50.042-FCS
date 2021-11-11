import random as r
from ex2 import *

class Alice:

    def __init__(self):
        self.pub = get_key('mykey.pem.pub')
        self.s = r.getrandbits(1024)
        self.x = square_multiply(self.s, self.pub.e, self.pub.n)
        self.send_msg_sign_pair()

    def send_msg_sign_pair(self):
        Bob(self.x, self.s)

class Bob:
    def __init__(self, x, s):
        self.pub = get_key('mykey.pem.pub')
        self.x_prime = square_multiply(s, self.pub.e, self.pub.n)
        self.check_s_is_valid(x, s)

    def check_s_is_valid(self, x, s):
        if self.x_prime == x:
            print(f's is a valid signature for message\n{x},\nBob accepts\n({x}, {s})')


if __name__ == "__main__":
    Alice()