"""
(Deprecated and unused)
This module offers basic connections between one client and one server.

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""

import json
import socket


def sock_init(port_num):
    """Initialize a scoket that listens on port_num."""
    server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port_num))
    server_socket.listen(10)
    # cancel the timeout of 3 seconds
    # server_socket.settimeout(3)
    return server_socket


def recv_data(ssocket):
    """Note that this only allows one end to send any data."""
    # receive a header which contains the size of msg
    # print('Receiving data header...')
    try:
        csock, dummy = ssocket.accept()
        header = csock.recv(1024).decode()
    except socket.timeout:
        print('Error: failed to receive data!')
    size = json.loads(header)['size']
    csock.close()
    # print('size =', size)

    # receive the actual data
    # print('Receiving some data...')
    try:
        csock, dummy = ssocket.accept()
        data = csock.recv(size).decode()
    except socket.timeout:
        print('Error: failed to receive data!')
    data = json.loads(data)
    csock.close()
    # print(data['data'])

    return data['data']


def send_data(target_port, data):
    """Send data to the target port."""
    msg = json.dumps({'data':data})
    sz = len(msg)
    # send a header indicating the size
    try:
        temp_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.connect(("localhost", target_port))
        header = {'size': sz}
        header_msg = json.dumps(header)
        temp_socket.send(header_msg.encode())
        temp_socket.close()
    except socket.error:
        print('Error: failed to send header!')

    # send the actual data to the target port
    try:
        temp_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.connect(("localhost", target_port))
        temp_socket.send(msg.encode())
        temp_socket.close()
    except socket.error:
        print('Error: failed to send data!')
