#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Servidor SIP
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
        lines = []
        for line in self.rfile:
            lines.append(line)

        for typeline in range(len(lines)):
            line = lines[typeline]

            if line[0] != 10 and (line[0] != 13 or line[1] != 10):
                client = line.decode('utf-8').split()

            if client[0] == 'REGISTER':
                nxtline = lines[typeline + 1]
                if nxtline[0] != 10 and (nxtline[0] != 13 or nxtline[1] != 10):
                    direction = client[1][client[1].rfind(':')+1:]
                    listclient = list(self.client_address)
                    timeclient = nxtline.decode('utf-8').split()
                    if timeclient[0] == 'Expires:' and int(timeclient[1]) == 0:
                        del self.dicclient[direction]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    else:
                        self.dicclient[direction] = listclient[0]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

        print(self.dicclient)

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
