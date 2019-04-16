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
# from Crypto.Cipher import AES
# from Crypto import Random


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
    kd = k[0]
    kc = k[1]
    kl = k[2]
    k1 = k[3]
    k2 = k[4]
    k3 = k[5]
    k4 = k[6]
    dictionary = {}
    nodes = []
    tree.get_nodes(tree.root, nodes)
    for node in nodes:
        children = []
        g2 = []
        for child in node.children:
            children.append(child)
            h2 = hashlib.blake2b(key = k2, digest_size = LAMBDA)
            h2.update(child.get_initial_path().encode('utf-8'))
            g2.append(h2.hexdigest().encode('utf-8'))
        for i in range(len(children) + 1, 129):
            g2.append(random.randint(1, 2) - 1)
        piu = [i for i in range(0, 128)]
        random.shuffle(piu)
        f2 = [i for i in range(0, 128)]
        for i in range(0, 128):
            f2[i] = g2[piu[i]]
        h1 = hashlib.blake2b(key = k1, digest_size = LAMBDA)
        h1.update(child.get_initial_path().encode('utf-8'))
        f1 = h1.hexdigest().encode('utf-8')
        xu = str(node.get_ind()) + '$' + str(tree.get_leafpos(node)) + '$' + str(tree.get_num(node)) + '$' + str(node.get_len()) + '$' + str(f1)
        for i in range(0, 128):
            xu += '$' + str(f2[i])
        # iv = Random.new().read(AES.block_size)
        # cipher = AES.new(kd, AES.MODE_CFB, iv)
        # wu = iv + cipher.encrypt(xu)


def main():
    encrypt(key_gen(), "hello")


if __name__ == '__main__':
    main()
