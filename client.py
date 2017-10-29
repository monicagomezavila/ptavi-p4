#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor y manda un mensaje SIP
"""

import sys
import socket

if len(sys.argv) != 6:
    print('Usage: client.py ip puerto register sip_address expires_value')
    sys.exit()

# Dirección IP del servidor y contenido a enviar.
SERVER = str(sys.argv[1])
PORT = int(sys.argv[2])
z = (sys.argv[3:])

LINE = ''
if sys.argv[3] == 'register':
    LINE += ('REGISTER sip:' + sys.argv[4] + ' SIP/2.0\r\n')
    LINE += ('Expires: ' + sys.argv[5] + '\r\n\r\n')
else:
    for elemento in z:
        LINE += elemento + ' '
        LINE = LINE[:LINE.rfind(' ')]

if int(sys.argv[5]) < 0:
    sys.exit('El tiempo debe ser >= 0')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto.
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
