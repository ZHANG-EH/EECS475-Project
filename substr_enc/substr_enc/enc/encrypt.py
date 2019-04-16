"""
Implementation of Enc function in the paper.

Jiangchen Zhu  <zjcsjtu@umich.edu>
Enhao Zhang    <ehzhang@umich.edu>
Zhiqi Chen     <zhiqich@umich.edu>
"""
from substr_enc.utils import Node, SuffixTree
from substr_enc.model import LAMBDA
import random
import secrets
import hashlib


def key_gen():
    """Generate the keys according to paper."""
    # LAMBDA is 64
    print(LAMBDA)
    key_list = []
    for i in range(7):
        key_list.append(secrets.token_bytes(LAMBDA))
    return key_list


def encrypt(k, s):
    """Implement an Enc function in the paper."""
    # build a tree upon the string s
    tree = SuffixTree(s)
    print('hi')
    kd = k[0]
    kc = k[1]
    kl = k[2]
    k1 = k[3]
    k2 = k[4]
    k3 = k[5]
    k4 = k[6]
    nodes = []
    tree.get_nodes(tree.root, nodes)
    for i in nodes:
        print(i.edge_label)
    h = hashlib.blake2b(key = k[1], digest_size = 64)
    h.update(s.encode('utf-8'))
    return h.hexdigest().encode('utf-8')


def main():
    encrypt(key_gen(), "hello")


if __name__ == '__main__':
    main()
