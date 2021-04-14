"""
Archivo ejecutable por parte del cliente de chat
"""

import socket, threading

# Se instancian las constantes con la direccion IP y el Puerto del servidor
HOST = '127.0.0.1'
PORT = 65432

# Funcion que se ejecuta en un nuevo hilo para recibir mensajes por parte del servidor
def receiveMessages(conn):
    while True:
        try:
            messageRecv = conn.recv(1024)

            if messageRecv:
                print(messageRecv.decode())
            else:
                conn.close()
                break

        except:
            print('Error al recibir mensaje del servidor')
            conn.close()
            break

# Programa principal que instancia el socket, crea el nuevo hilo para escuchar el chat y recibe input para enviar mensajes
try:
    sock = socket.socket()
    sock.connect((HOST, PORT))

    newThread = threading.Thread(target=receiveMessages, args=[sock])
    newThread.start()

    print('Establecida la conexión con el servidor', HOST, PORT)

    while True:
        sendMessage = input()

        if sendMessage == 'salir':
            break

        sock.send(sendMessage.encode())

    sock.close()

except:
    print('Error al conectar con el servidor')
    sock.close()