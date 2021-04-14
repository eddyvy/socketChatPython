"""
Archivo ejecutable por parte del servidor de chat
"""

import socket, threading

# Se instancian las constantes con la direccion IP y el Puerto del servidor
HOST = '10.10.1.1'
PORT = 2018

# Se declara la lista con los sockets conectados al servidor
connections = []

# Funcion para eliminar una conexion del servidor
def delConnection(conn):
    if conn in connections:
        conn.close()
        connections.remove(conn)

# Funcion para enviar los pensajes a todas las conexiones
def showMessage(message):
    for clientConn in connections:
        try:
            clientConn.send(message.encode())

        except:
            print('Error al enviar el mensaje')
            delConnection(clientConn)

# Funcion para manejar la conexion y recibir mensajes
def useConnection(conn, addr):
    while True:
        try:
            messageRecv = conn.recv(1024)

            if messageRecv:
                messageSigned = str(addr[1]) + ' - ' + messageRecv.decode()
                print(messageSigned)
                
                showMessage(messageSigned)
            else:
                delConnection(conn)
                break

        except:
            print('Hubo un error al conectar')
            delConnection(conn)
            break

# Programa principal que instancia el socket e incia el servidor
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(7)

    print('El servidor está escuchando! IP:', HOST, 'Puerto:', PORT)
    
    # Bucle para aceptar conexiones y crear un nuevo hilo de ejecucion
    while True:
        clientConn, clientAddr = sock.accept()

        connections.append(clientConn)

        newThread = threading.Thread(target=useConnection, args=[clientConn, clientAddr])
        newThread.start()

except:
    print('Ha ocurrido un error :(')

finally:

    if len(connections) > 0:
        for clientConn in connections:
            delConnection(clientConn)

    sock.close()
