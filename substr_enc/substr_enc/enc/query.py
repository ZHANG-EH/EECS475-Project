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
import hmac

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
        h = hmac.new(key = k1, digestmod = hashlib.sha256)
        h.update(prefix_p.encode('utf-8'))
        f1 = h.digest()
        # f2
        h = hmac.new(key = k2, digestmod = hashlib.sha256)
        h.update(prefix_p.encode('utf-8'))
        f2 = h.digest()
        # T
        iv = Random.new().read(AES.block_size)
        obj = AES.new(f2, AES.MODE_CFB, iv)
        t_list.append(iv.hex() + "$" + obj.encrypt(f1).hex())
    h = hmac.new(key = k1, digestmod = hashlib.sha256)
    emptystring = ''
    h.update(emptystring.encode('utf-8'))
    root = h.digest()
    # client returns (root, t_list)
    parsed_list = d[root].split("$")
    for i in range(m):
        for j in range(128):
            ivenc = t_list[i].split("$")
            iv = bytes.fromhex(ivenc[0])
            enc = bytes.fromhex(ivenc[1])
            obj = AES.new(bytes.fromhex(parsed_list[j]), AES.MODE_CFB, iv)
            try:
                plaintext = obj.decrypt(enc)
                # f1 != perp
                parsed_list = d[plaintext].split("$")
                break
            except ValueError:
                print("Key incorrect or message corrupted")
            except KeyError:
                # print("wrong decryption")
                continue
    iv = bytes.fromhex(parsed_list[128])
    encW = bytes.fromhex(parsed_list[129])
    # server sends W (encW)
    obj = AES.new(kd, AES.MODE_CFB, iv)
    try:
        X = str(obj.decrypt(encW), "utf-8")
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
    h = hmac.new(key = k1, digestmod = hashlib.sha256)
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
                # return "No result: perp"
            except:
                continue
    if ind == -1:
        return "no matching query found"
    m_seq = [i for i in range(0, m)]
    random.shuffle(m_seq)
    x_list = list(repeat(0, m))
    for i in range(m):
        random.seed(k3)
        prp_list = [i for i in range(0, len(c))]
        random.shuffle(prp_list)
        if ind + i >= len(c):
            return "no matching query found"
        x_list[m_seq[i]] = prp_list[ind + i]
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
            Y = str(obj.decrypt(encC), "utf-8")
        except ValueError:
            return "No result: perp"
        parsed_Y = Y.split("$")
        if int(parsed_Y[1]) != ind + i:
            return "No result: perp"
        if parsed_Y[0] != p[i]:
            return "no matching query found"
    num_seq = [i for i in range(0, num)]
    random.shuffle(num_seq)
    y_list = list(repeat(0, num))
    for i in range(num):
        random.seed(k4)
        prp_list = [i for i in range(0, len(c))]
        random.shuffle(prp_list)
        y_list[num_seq[i]] = prp_list[leafpos + i]
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
            dectext = str(obj.decrypt(encL), "utf-8")
        except ValueError:
            return "No result: perp"
        parsed_dec = dectext.split("$")
        if int(parsed_dec[1]) != leafpos + i:
            return "No result: perp"
        A_list.append(parsed_dec[0])
    A_list = list(map(int, A_list))
    A_list = sorted(A_list)
    return A_list
