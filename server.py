"""
Simple usage of module substr_enc.conn

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""

import substr_enc.conn as sc


def main():
    """A simple server answers clients questions."""
    # listen on port 6000
    sock = sc.sock_init(6000)
    # block until it receives a question
    question = sc.recv_data(sock)
    print('Received:', question)
    # send a feedback to port 6001
    feedback = "Please give me some choices!"
    print('Sending:', feedback)
    sc.send_data(6001, feedback)
    # receive choices
    choices = sc.recv_data(sock)
    print('Received:', choices)
    # send the answer
    answer = "My favorite is " + str(choices[0])
    print('Sending:', answer)
    sc.send_data(6001, answer)


if __name__ == '__main__':
    main()
