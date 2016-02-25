#!/usr/bin/python2
"""Server main class."""

import socket


class HttpServer:
    """Server object."""

    def __init__(self, port=5000):
        """Constructor."""
        self.host = "localhost"
        self.port = port
        self.data = ""

    def serve(self):
        """Main loop."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print "start server on:", self.host, self.port

        while True:

            self.conn, self.addr = self.socket.accept()
            self.conn.settimeout(0.5)
            print "got connection from:", self.addr

            c = HttpConnection(self.conn)
            c.connection()

            parse = HttpRequestParser(c.data)
            parse.get_request()

            parse.request.test()  # only for me

            c.conn.send(c.data)
            c.conn.close()


class HttpConnection:
    """New connection."""

    def __init__(self, conn):
        """Constructor."""
        self.conn = conn
        self.data = ""

    def connection(self):
        """Read data from connection."""
        try:
            while True:
                temp = self.conn.recv(1024)
                self.data += temp
                if not temp:
                    break
        except socket.timeout:
            pass
        print self.data
        print self.data.split("\n\n")  # only for me!


class HttpRequest:
    """Parser."""

    def __init__(self, method, headers, body):
        """Constructor."""
        self.method = method
        self.headers = headers
        self.body = body

    def test(self):  # only for me!
        """Test."""
        print "-----------"
        print self.method
        print "-----------"
        print self.headers
        print "-----------"
        print self.body
        print "-----------\n\n\n"


class HttpRequestParser:
    """Request parser."""

    def __init__(self, data):
        """Constructor."""
        self.data = data
        self.head = data.split("\r\n\r\n")[0]
        self.headers = {}
        self.body = []

    def __get_method(self):
        """Method string."""
        self.method = self.head.split(" ")[0]

    def __get_headers(self):
        """Header dictionary."""
        for i in self.head.splitlines():
            try:
                temp = i.split(": ")
                self.headers[temp[0]] = temp[1]
            except IndexError:
                pass

    def __get_body(self):
        """Body list."""
        try:
            self.body = self.data.split("\r\n\r\n")[1]
        except IndexError:
            pass

    def get_request(self):
        """Make request."""
        self.__get_method()
        self.__get_headers()
        self.__get_body()
        self.request = HttpRequest(self.method,
                                   self.headers,
                                   self.body)

s = HttpServer()
s.serve()
