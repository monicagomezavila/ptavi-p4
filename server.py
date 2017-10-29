#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dicclient = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion \n")

        for line in self.rfile:

            if line[0] != 10 and (line[0] != 13 or line[1] != 10):
                print("El cliente nos manda ", line.decode('utf-8'))
                client = line.decode('utf-8').split()

                if client[0] == 'REGISTER' and client[2] == 'SIP/2.0':
                        direction = client[1][client[1].rfind(':')+1:]
                        listclient = list(self.client_address)
                        self.dicclient[direction] = listclient[0]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                        print(listclient)
        print(self.dicclient)
        print('\r')

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
