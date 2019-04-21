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
    # print("root: ", root)
    parsed_list = d[root].split("$")
    # print("parsed_list length: (should be d + 1) ", len(parsed_list))
    for i in range(m):
        for j in range(128):
            ivenc = t_list[i].split("$")
            iv = bytes.fromhex(ivenc[0])
            enc = bytes.fromhex(ivenc[1])
            # print("parsed_list: ", parsed_list[j])
            # print("len: ", len(parsed_list[j]))
            obj = AES.new(bytes.fromhex(parsed_list[j]), AES.MODE_CFB, iv)
            try:
                plaintext = obj.decrypt(enc)
                # print("plaintext: ", plaintext)
                # f1 != perp
                parsed_list = d[plaintext].split("$")
                # print("plaintext: ", i, j)
                # print("success")
                break
            except ValueError:
                print("Key incorrect or message corrupted")
            except KeyError:
                print("wrong decryption")
    iv = bytes.fromhex(parsed_list[128])
    # print("iv: ", iv)
    encW = bytes.fromhex(parsed_list[129])
    # print("encW: ", encW)
    # print("encW: ", encW)
    # print("encW: ", encW) # encW = cipher.encrypt(xu)
    # server sends W (encW)
    obj = AES.new(kd, AES.MODE_CFB, iv)
    try:
        X = str(obj.decrypt(encW), "utf-8")
    except ValueError:
        # print("here")
        return "No result: perp"
    # X != perp
    # print("X: ", X)
    parsed_X = X.split("$")
    ind = int(parsed_X[0])
    # print("ind: ", ind)
    leafpos = int(parsed_X[1])
    # print("leafpos: ", leafpos)
    num = int(parsed_X[2])
    # print("num: ", num)
    lenvar = int(parsed_X[3])
    # print("lenvar: ", lenvar)
    f1 = bytes.fromhex(parsed_X[4])
    f_list = parsed_X[5:]
    h = hashlib.blake2b(key = k1, digest_size = LAMBDA)
    subp = p[:lenvar]
    # print("subp: ", subp)
    h.update(subp.encode('utf-8'))
    if f1 != h.digest():
        # print("here")
        return "No result: perp"
    for j in range(lenvar, m):
        for i in range(0, 128):
            ivencT = t_list[j].split("$")
            iv = bytes.fromhex(ivencT[0])
            encT = bytes.fromhex(ivencT[1])
            obj = AES.new(bytes.fromhex(f_list[i]), AES.MODE_CFB, iv)
            try:
                X = obj.decrypt(encT)
                # print("X: ", X)
                # print("here")
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
            # print("Y: ", Y)
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
        # print("dectext: ", dectext)
        parsed_dec = dectext.split("$")
        if int(parsed_dec[1]) != leafpos + i:
            return "No result: perp"
        A_list.append(parsed_dec[0])
    A_list = list(map(int, A_list))
    A_list = sorted(A_list)
    return A_list


def main():
    key_list = key_gen()
    d, c, l = encrypt(key_list, "Section 1. All persons born or naturalized in the United States, and subject to the jurisdiction thereof, are citizens of the United States and of the State wherein they reside. No State shall make or enforce any law which shall abridge the privileges or immunities of citizens of the United States; nor shall any State deprive any person of life, liberty, or property, without due process of law; nor deny to any person within its jurisdiction the equal protection of the laws. Section 2. Representatives shall be apportioned among the several States according to their respective numbers, counting the whole number of persons in each State, excluding Indians not taxed. But when the right to vote at any election for the choice of electors for President and Vice President of the United States, Representatives in Congress, the Executive and Judicial officers of a State, or the members of the Legislature thereof, is denied to any of the male inhabitants of such State, being twenty-one years of age, and citizens of the United States, or in any way abridged, except for participation in rebellion, or other crime, the basis of representation therein shall be reduced in the proportion which the number of such male citizens shall bear to the whole number of male citizens twenty-one years of age in such State. Section 3. No person shall be a Senator or Representative in Congress, or elector of President and Vice President, or hold any office, civil or military, under the United States, or under any State, who, having previously taken an oath, as a member of Congress, or as an officer of the United States, or as a member of any State legislature, or as an executive or judicial officer of any State, to support the Constitution of the United States, shall have engaged in insurrection or rebellion against the same, or given aid or comfort to the enemies thereof. But Congress may, by a vote of two-thirds of each House, remove such disability. Section 4. The validity of the public debt of the United States, authorized by law, including debts incurred for payment of pensions and bounties for services in suppressing insurrection or rebellion, shall not be questioned. But neither the United States nor any State shall assume or pay any debt or obligation incurred in aid of insurrection or rebellion against the United States, or any claim for the loss or emancipation of any slave; but all such debts, obligations and claims shall be held illegal and void. Section 5. The Congress shall have power to enforce, by appropriate legislation, the provisions of this article.")
    result = query_client(key_list, "Section", d, c, l)
    print("result: ", result)

if __name__ == '__main__':
    main()
