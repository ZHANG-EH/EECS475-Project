"""
Implementation of Enc function in the paper.

Jiangchen Zhu  <zjcsjtu@umich.edu>
Enhao Zhang    <ehzhang@umich.edu>
"""
from substr_enc.utils import Node, SuffixTree
from substr_enc.model import LAMBDA
import random


def key_gen():
    """Generate the keys according to paper."""
    # LAMBDA is 64
    print(LAMBDA)



def encrypt(k, s):
    """Implement an Enc function in the paper."""
    # build a tree upon the string s
    tree = SuffixTree(s)
    print('hi')
    