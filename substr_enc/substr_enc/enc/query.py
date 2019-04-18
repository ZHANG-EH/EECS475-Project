"""
Implementation of Query function in the paper.

Jiangchen Zhu  <zjcsjtu@umich.edu>
Enhao Zhang    <ehzhang@umich.edu>
Zhiqi Chen     <zhiqich@umich.edu>
"""

from substr_enc.utils import Node, SuffixTree
from substr_enc.model import LAMBDA
from substr_enc.enc import key_gen, encrypt
from Crypto.Cipher import AES
from Crypto import Random
from itertools import repeat
import hashlib
import random

def query_client(k, p, d, c, l):
    kd = k[0]
    kc = k[1]
    kl = k[2]
    k1 = k[3]
    k2 = k[4]
    k3 = k[5]
    k4 = k[6]
    m = len(p)
    t_list = []
    for i in range(m):
        prefix_p = p[:(i+1)]
        # f1
        h = hashlib.blake2b(key = k1, digest_size = LAMBDA)
        h.update(prefix_p.encode('utf-8'))
        f1 = h.digest()
        # print(f1)
        # f2
        h = hashlib.blake2b(key = k2, digest_size = LAMBDA)
        # print(h.digest_size)
        h.update(prefix_p.encode('utf-8'))
        f2 = h.digest()
        # print(f2)
        # T
        iv = Random.new().read(AES.block_size)
        obj = AES.new(f2, AES.MODE_CFB, iv)
        # print("T = ", str(iv) + "$" + str(obj.encrypt(f1)))
        t_list.append(iv.hex() + "$" + obj.encrypt(f1).hex())
    h = hashlib.blake2b(key = k1, digest_size = LAMBDA)
    emptystring = ''
    h.update(emptystring.encode('utf-8'))
    root = h.digest()
    # client returns (root, t_list)
    print("root: ", root)
    parsed_list = d[root].split("$")
    print("parsed_list length: (should be d + 1) ", len(parsed_list))
    for i in range(m):
        for j in range(128):
            ivenc = t_list[i].split("$")
            iv = bytes.fromhex(ivenc[0])
            enc = bytes.fromhex(ivenc[1])
            print("parsed_list: ", parsed_list[j])
            print("len: ", len(parsed_list[j]))
            obj = AES.new(bytes.fromhex(parsed_list[j]), AES.MODE_CFB, iv)
            try:
                plaintext = obj.decrypt(enc)
                # f1 != perp
                parsed_list = d[plaintext].split("$")
                break
            except ValueError:
                print("Key incorrect or message corrupted")
    W = parsed_list[128]
    # server returns W
    ivencW = W.split("$")
    iv = bytes.fromhex(ivencW[0])
    encW = bytes.fromhex(ivencW[1])
    obj = AES.new(kd, AES.MODE_CFB, iv)
    try:
        X = obj.decrypt(encW)
    except ValueError:
        return "No result: perp"
    # X != perp
    parsed_X = X.split("$")
    ind = int(parsed_X[0])
    leafpos = int(parsed_X[1])
    num = int(parsed_X[2])
    lenvar = int(parsed_X[3])
    f1 = bytes.fromhex(parsed_X[4])
    f_list = parsed_X[5:]
    h = hashlib.blake2b(key = k1, digest_size = LAMBDA)
    subp = p[:lenvar]
    h.update(subp.encode('utf-8'))
    if f1 != h.digest():
        return "No result: perp"
    for j in range(lenvar, m):
        for i in range(0, 128):
            ivencT = t_list[j].split("$")
            iv = bytes.fromhex(ivencT[0])
            encT = bytes.fromhex(ivencT[1])
            obj = AES.new(bytes.fromhex(f_list[i]), AES.MODE_CFB, iv)
            try:
                X = obj.decrypt(encT)
                return "No result: perp"
            except ValueError:
                continue
    if ind == 0:
        return "empty string"
    m_seq = [i for i in range(0, m)]
    random.shuffle(m_seq)
    x_list = list(repeat(0, m))
    for i in range(m):
        random.seed(k3)
        prp_list = [i for i in range(0, len(c))]
        random.shuffle(prp_list)
        x_list[m_seq[i]] = prp_list[ind + i - 1]
    # client sends x_list, i.e. (x1, ..., xm)
    c_list = [i for i in range(0, m)]
    for i in range(m):
        c_list[i] = c[x_list[i]]
    # server sends c_list, i.e. (c1, ..., cm)
    for i in range(m):
        ivencC = c_list[m_seq[i]].split("$")
        iv = bytes.fromhex(ivencC[0])
        encC = bytes.fromhex(ivencC[1])
        obj = AES.new(kc, AES.MODE_CFB, iv)
        try:
            Y = obj.decrypt(encC)
        except ValueError:
            return "No result: perp"
        parsed_Y = Y.split("$")
        if int(parsed_Y[1]) != ind + i - 1:
            return "No result: perp"
        if parsed_Y[0] != p[i]:
            return "empty string"
    num_seq = [i for i in range(0, num)]
    random.shuffle(num_seq)
    y_list = list(repeat(0, num))
    for i in range(num):
        random.seed(k4)
        prp_list = [i for i in range(0, len(c))]
        random.shuffle(prp_list)
        y_list[num_seq[i]] = prp_list[leafpos + i - 1]
    # client sends y_list, i.e. (y1, ..., ynum)
    L_list = list(repeat(0, num))
    for i in range(num):
        L_list[i] = l[y_list[i]]
    # server sends L_list, i.e. (L1, ..., Lnum)
    A_list = []
    for i in range(num):
        ivencL = L_list[num_seq[i]].split("$")
        iv = bytes.fromhex(ivencL[0])
        encL = bytes.fromhex(ivencL[1])
        obj = AES.new(kl, AES.MODE_CFB, iv)
        try:
            dectext = obj.decrypt(encL)
        except ValueError:
            return "No result: perp"
        parsed_dec = dectext.split("$")
        if int(arsed_dec[1]) != leafpos + i - 1:
            return "No result: perp"
        A_list.append(parsed_dec[0])
    return A_list


def main():
    key_list = key_gen()
    d, c, l = encrypt(key_list, "hello")
    query_client(key_list, "string", d, c, l)


if __name__ == '__main__':
    main()
