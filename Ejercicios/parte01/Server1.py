import socket


def chat_with(dict_connections):
    socketClienteA = dict_connections[1]['conn']
    socketClienteB = dict_connections[2]['conn']

    nameClienteA = dict_connections[1]['from']
    nameClienteB = dict_connections[2]['from']

    while True:
        data = None
        while data is None:
            data = socketClienteA.recv(1024)

        texto_clienteA = data.decode('ASCII')

        data = None
        while data is None:
            data = socketClienteB.recv(1024)

        texto_clienteB = data.decode('ASCII')

        dato_A = str(nameClienteA) + " says: " + texto_clienteA
        dato_B = str(nameClienteB) + " says: " + texto_clienteB

        socketClienteB.sendall(dato_A.encode('ASCII'))
        socketClienteA.sendall(dato_B.encode('ASCII'))

if __name__ == "__main__":
    port_number = 10023
    bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bindsocket.bind(('', port_number))
    bindsocket.listen(2)
    fromaddr = None

    IDClientes = ['00205604','00204686']
    BannerID = '00205950'

    print("Servidor escuchando en puerto: " + str(port_number))

    dict_conn = {}

    count = 0
    while True:
        try:
            newsocket, fromaddr = bindsocket.accept()
            data = newsocket.recv(1024).decode('ASCII')
            print(f"Conexión recibida de: {data}")
            clientInfo = data.split('|')
            if clientInfo[0] in IDClientes:
                dict_conn[data] = {'from': fromaddr, 'conn': newsocket}
                count += 1
                newsocket.sendall(f'{BannerID} OK'.encode('ASCII'))
                while True:
                    msg = None
                    while msg is None:
                        msg = newsocket.recv(1024)
                    print(msg.decode('ASCII'))
                    if 'LIST' in msg.decode('ASCII'):
                        list = f'IDServidor|{len(dict_conn)}'
                        newsocket.sendall(list.encode('ASCII'))
                    elif 'EXIT' in msg.decode('ASCII'):
                        newsocket.sendall('IDServidor|EXIT_OK'.encode('ASCII'))
                        newsocket.close()
                        print(f"Conexión cerrada con: {data}")
                        del dict_conn[data]
                        break
                    else:
                        newsocket.sendall('IDServidor|MESSAGE_RECEIVED'.encode('ASCII'))
            else:
                newsocket.sendall(f'{BannerID} NO'.encode('ASCII'))
                newsocket.close()
                print(f"BannerID inválido. Conexión cerrada con: {data}")
        except KeyboardInterrupt:
            break

    print("xd")
    chat_with(dict_conn)

