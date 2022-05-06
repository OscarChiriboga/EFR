import socket
import sys


ServerIP = '172.21.13.147'
ServerPort = 10023

#IDCliente|IP
IDCliente = '00205604'
IP = socket.gethostbyname("rpi3.local")

print(f"Establishing connection from {IP} to {ServerIP}:{ServerPort}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.settimeout(960.0)
s.connect((ServerIP, ServerPort))
s.settimeout(None)


if s is not None:
    clientInfo = f'{IDCliente}|{IP}'
    s.sendall(clientInfo.encode('ASCII'))
    data = None
    while data is None:
        data = s.recv(1024)
    print(data.decode('ASCII'))
    if 'OK' in data.decode('ASCII'):
        while True:
            data = input('Tu: ')
            s.sendall(f'{IDCliente}|{data}'.encode('ASCII'))
            data = None
            while data is None:
                data = s.recv(1024)
            print(data.decode('ASCII'))
            if 'EXIT_OK' in data.decode('ASCII'):
                s.close()
                print('Conexión con servidor cerrada')
                break
    else:
        print('BannerID inválido. Conexión con servidor cerrada')
        s.close()

