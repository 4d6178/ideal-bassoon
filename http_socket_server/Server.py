#!/usr/bin/python2

import socket
import time
import Handler
raw = '\n\n'


class HttpServer:

    def __init__(self):
        self.host = ''
        self.port = 5000

    def activate_server(self):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM,
                                    socket.IPPROTO_TCP)
        try:
            self.socket.setsockopt(socket.SOL_SOCKET,
                                   socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.__serve()
        except socket.error as msg:
            print 'Oops! we have an error here...\n', msg
            return

    def __serve(self):
        while True:
            print 'Awaiting new connection\n'
            client_sock, client_addr = self.socket.accept()
            print 'Got connection from', client_addr

            self.data = client_sock.recv(2048)
            try:
                Handler.handle()
            finally:
                client_sock.close()


# class HttpConnection:


s = HttpServer()
s.activate_server()
