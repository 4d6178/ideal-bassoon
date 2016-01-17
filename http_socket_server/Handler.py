#!/usr/bin/python2

import socket
import Server


class HttpHandler:

    def handle(self):
        print 'this is handler'
        print Server.HttpServer.data
        pass
