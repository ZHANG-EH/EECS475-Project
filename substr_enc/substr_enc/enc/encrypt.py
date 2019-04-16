"""
Implementation of Enc function in the paper.

Jiangchen Zhu  <zjcsjtu@umich.edu>
Enhao Zhang    <ehzhang@umich.edu>
"""
from substr_enc.utils import Node, SuffixTree
from substr_enc.model import LAMBDA
import random
import secrets


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


# def main():
#     key_gen()
#
#
# if __name__ == '__main__':
#     main()
