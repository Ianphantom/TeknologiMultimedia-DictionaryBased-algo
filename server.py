#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime
from socket import error as SocketError
from random import randint
basename = "checkCompressed.lzw"
import os
import errno
import time

imgcounter = 1


HOST = '127.0.0.1'
PORT = 6662

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)

while True:

    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:
        if sock == server_socket:

            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)

        else:

            try:
                data = sock.recv(4096)
                txt = str(data)

                if data:

                    if data.startswith('SIZE'):
                        tmp = txt.split()
                        size = int(tmp[1])

                        print 'got size'

                        sock.sendall("GOT SIZE")

                    elif data.startswith('BYE'):
                        sock.shutdown()

                    else :

                        myfile = open(basename, 'wb')
                        myfile.write(data)

                        data = sock.recv(40960000)
                        if not data:
                            myfile.close()
                            break
                        myfile.write(data)
                        time.sleep(20)
                        myfile.close()

                        sock.sendall("GOT IMAGE")
                        sock.shutdown(0)
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    raise
                pass
        imgcounter += 1
server_socket.close()