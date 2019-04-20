"""
Simple usage of module substr_enc.conn

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""

import substr_enc.conn as sc


# A couple of notes:
# Run the server.py first
# You must specify a port number to sock_init
# The function recv_data() will block until it receives some data.

def main():
    """A simple client asks server a question."""
    # listen on port 6001
    sock = sc.sock_init(6001)
    question = "Hey, tell me your favorite fruit!"
    # send the question string to port 6000
    print('Sending:', question)
    sc.send_data(6000, question)
    # receive a response
    response = sc.recv_data(sock)
    print('Received:', response)
    # send another list to port 6000
    choices = ['apple', 'banana', 'orange']
    print('Sending:', choices)
    sc.send_data(6000, choices)
    # receive a response
    response = sc.recv_data(sock)
    print('Received:', response)


if __name__ == '__main__':
    main()
