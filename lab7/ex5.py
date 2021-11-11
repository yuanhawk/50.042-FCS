# Pycrypto is running a deprecated version of time module. Edit time.clock() to time.time() to get package running
from ex2 import get_key, square_multiply
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS

def generate_RSA(bits=1024):
    key = RSA.generate(bits)
    f = open('ex5.pem.pub', 'wb')
    f.write(key.publickey().exportKey('PEM'))
    f.close()
    g = open('ex5.pem.priv', 'wb')
    g.write(key.exportKey('PEM'))
    g.close()

def encrypt(key_file, num):
    pub = RSA.importKey(open(key_file).read())
    cipher = PKCS1_OAEP.new(pub)
    ciphertext = cipher.encrypt(num.encode())
    return int.from_bytes(ciphertext, 'big')

def encrypt_RSA(key_file, message):
    pub = RSA.importKey(open(key_file).read())
    cipher = PKCS1_OAEP.new(pub)
    with open(message, 'rb') as fin:
        ciphertext = cipher.encrypt(fin.read())
        return ciphertext

def decrypt_RSA(key_file, ciphertext):
    priv = RSA.importKey(open(key_file).read())
    cipher = PKCS1_OAEP.new(priv)
    message = cipher.decrypt(ciphertext).decode()
    print("Plaintext is: ", message)
    return message

def sign_data(key_file, data):
    priv = RSA.importKey(open(key_file).read())
    h = SHA256.new()
    with open(data, 'rb') as fin:
        h.update(fin.read())
    signer = PKCS1_PSS.new(priv)
    signature = signer.sign(h)
    return signature


def verify_sign(key_file, sign, data):
    pub = RSA.importKey(open(key_file).read())
    h = SHA256.new()
    with open(data, 'rb') as fin:
        h.update(fin.read())
    verifier = PKCS1_PSS.new(pub)
    if verifier.verify(h, sign):
        return True
    return False


if __name__ == "__main__":
    generate_RSA()
    e = encrypt_RSA('ex5.pem.pub', 'mydata.txt')
    decrypt_RSA('ex5.pem.priv', e)

    signature = sign_data('ex5.pem.priv', 'mydata.txt')
    if verify_sign('ex5.pem.pub', signature, 'mydata.txt'):
        print ("The signature is authentic.")
    else:
        print ("The signature is not authentic.")

    # RSA protocol attack

    i = 100
    print('Part V-------------')
    print('Encrypting: ', i)
    y = encrypt('ex5.pem.pub', '100')
    print('Result:\n', y)
    pub = get_key('ex5.pem.pub')
    ys = square_multiply(2, pub.e, pub.n)
    m = (y * ys) % pub.n
    print('Modified to:\n', m)
    # d = decrypt_RSA('ex5.pem.priv', m)


    try:
        d = decrypt_RSA('ex5.pem.priv', str(m).encode())
        print('Decrypted: ', d)
        pass
        #decrypted_m = decrypt_RSA("my_private_key.pem", m)
        #print("Decrypted: " + str(decrypted_m))
    except ValueError as e:
        print("Decryption failed")
        print(e)

