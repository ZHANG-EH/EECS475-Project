"""
Implementation of Query function in the paper.

Jiangchen Zhu  <zjcsjtu@umich.edu>
Enhao Zhang    <ehzhang@umich.edu>
Zhiqi Chen     <zhiqich@umich.edu>
"""

from substr_enc.utils import Node, SuffixTree
from substr_enc.model import LAMBDA
from substr_enc.enc import key_gen
from Crypto.Cipher import AES
from Crypto import Random
import hashlib

def query_client(k, p, ct):
    kd = k[0]
    print(len(kd))
    kc = k[1]
    kl = k[2]
    k1 = k[3]
    k2 = k[4]
    k3 = k[5]
    k4 = k[6]
    d = ct[0]
    c = ct[1]
    l = ct[2]
    m = len(p)
    for i in range(m):
        prefix_p = p[:(i+1)]
        h = hashlib.blake2b(key = k1, digest_size = LAMBDA)
        h.update(prefix_p.encode('utf-8'))
        f1 = h.hexdigest().encode('utf-8')
        print(f1)
        h = hashlib.blake2b(key = k2, digest_size = LAMBDA)
        h.update(prefix_p.encode('utf-8'))
        f2 = h.hexdigest().encode('utf-8')
        print(f2)
        print(len(f2))
        iv = Random.new().read(AES.block_size)
        obj = AES.new(f2, AES.MODE_CBC, iv)
        t = iv + obj.encrypt(f1)
        h = hashlib.blake2b(key = k1, digest_size = LAMBDA)
        emptystring = ''
        h.update(emptystring.encode('utf-8'))
        root = h.hexdigest().encode('utf-8')

def main():
    query_client(key_gen(), "string", [0,0,0])


if __name__ == '__main__':
    main()
