#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Servidor SIP
"""

import socketserver
import json
import time
import os.path
from pprint import pprint


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dicclient = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.json2registered()
        lines = []
        infouser = []

        for line in self.rfile:
            lines.append(line)

        for typeline in range(len(lines)):
            line = lines[typeline]

            if line[0] != 10 and (line[0] != 13 or line[1] != 10):
                client = line.decode('utf-8').split()

            if client[0] == 'REGISTER':
                nxtline = lines[typeline + 1]

                if nxtline[0] != 10 and (nxtline[0] != 13 or nxtline[1] != 10):
                    user = client[1][client[1].rfind(':')+1:]
                    listclient = list(self.client_address)
                    timeclient = nxtline.decode('utf-8').split()

                    if timeclient[0] == 'Expires:' and int(timeclient[1]) == 0:
                        del self.diclient[user]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    else:
                        exdays = time.ctime(time.time() + int(timeclient[1]))
                        infouser = [listclient[0], exdays]
                        self.diclient[user] = infouser
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

            n = 1
            while n <= len(self.dicclient):
                for user in self.diclient:
                    now = time.ctime(time.time())
                    if self.diclient[user][1] <= now:
                        del self.diclient[user]
                        break
                n = n+1

        print(self.diclient)
        self.register2json()

    def register2json(self, fichjson='registered.json'):
        with open(fichjson, 'w') as outfile:
            json.dump(self.diclient, outfile, separators=(',', ':'), indent="")

    def json2registered(self):
        if os.path.exists('registered.json'):
            with open('registered.json') as data_file:
                data = json.load(data_file)
            self.diclient = data
        else:
            self.diclient = {}


if __name__ == "__main__":
    # Listens at localhost ('') port 5060
    # and calls the EchoHandler class to manage the request
    PUERTO = 5060
    serv = socketserver.UDPServer(('', PUERTO), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
