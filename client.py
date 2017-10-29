#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import sys
import socket


# Constantes. Dirección IP del servidor y contenido a enviar.
SERVER = str(sys.argv[1])
PORT = int(sys.argv[2])
z = (sys.argv[3:])
print(z)

LINE = ''
if sys.argv[3] == 'register':
    LINE += 'REGISTER sip:' + sys.argv[4] + ' SIP/2.0\r\n\r\n'

elif sys.argv[3] == 'REGISTER':
    for elemento in z:
        LINE += elemento + ' '
    LINE = LINE[:LINE.rfind(' ')]
    LINE = (LINE[:LINE.rfind('0')+1] + "\r\n\r\n")

else:
    sys.exit('El mensaje sip está mal formulado')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
