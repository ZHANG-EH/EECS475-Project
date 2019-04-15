# eecs475-project

## Instructions
- Create Python3 Virtual Environement
```shell
$ python3 -m venv env
$ source env/bin/activate
```
- Install the package
```shell
$ pip install -e substr_enc
```

- Run a test
```shell
$ python test.py
```

## Group Members
- Enhao Zhang
- Jiayi Fang
- Zhiqi Chen
- Jiangchen Zhu

## Proposal
We are going to build a software that implements the Substring-Searchable
Symmetric Encryption. Further, in the software we will simulate a client-and-server
interaction where client queries a string and server returns the result using this
encryption scheme. We will also discuss the efficiency and security of this encryption.

The encryption we will implement is based on this [paper](https://eprint.iacr.org/2014/638.pdf
).
