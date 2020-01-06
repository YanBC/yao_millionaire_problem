# https://research.cs.wisc.edu/areas/sec/yao1982-ocr.pdf


from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Util import number
import numpy as np

class Millionaire:
    def __init__(self, num_million, max_million=10, num_bits=2048):
        self.key = RSA.generate(2048)
        self.million = num_million
        self.max_million = max_million
        self.num_bits = num_bits


    def get_pub_key_pem(self):
        return self.key.publickey().exportKey('PEM')


    def get_ciphertext(self, peer_key_pem):
        peer_pubKey = RSA.importKey(peer_key_pem)
        self.x = number.getRandomNBitInteger(self.num_bits)
        k = peer_pubKey.encrypt(self.x, 0)[0]

        return k - self.million


    def get_batch_z(self, ciphertext):
        y_u = []
        for i in range(0, self.max_million):
            y_u.append(self.key.decrypt(ciphertext + i))

        while True:
            p = number.getPrime(self.num_bits//2)
            z_u = [y % p for y in y_u]

            row = np.array(z_u).reshape((1, len(z_u)))
            col = np.transpose(row)
            diff = np.abs(row - col)
            diff = diff + np.eye(len(z_u)) * 3
            if np.all(diff >= 2):
                break

        final_z_u = []
        for i, z in enumerate(z_u):
            if i >= self.million:
                z = (z + 1) % p
            final_z_u.append(z)
        return p, final_z_u


    def peer_is_richer(self, p, batch_z):
        box = batch_z[self.million]
        # peer is richer
        if self.x % p == box:
            return True
        # peer is less or equally wealthy
        else:
            return False




if __name__ == '__main__':
    Alice = Millionaire(8)
    Bob = Millionaire(5)

    Alice_pubKey = Alice.get_pub_key_pem()
    Bob_ciphertext = Bob.get_ciphertext(Alice_pubKey)
    Alice_p, Alice_batch_z = Alice.get_batch_z(Bob_ciphertext)

    result = Bob.peer_is_richer(Alice_p, Alice_batch_z)