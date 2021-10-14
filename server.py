#code mainly sourced and adapted from first tutorial link

import threading
import socket
import argparse
import os

class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print('Server is listening at ', sock.getsockname())

        #accepting new connections
        while True:
            conn, sockname = sock.accept()
            print('Accepted new connection from {} to {}'.format(conn.getpeername(), conn.getsockname()))
            #thread and starting thread
            server_socket = ServerSocket(conn, sockname, self)
            server_socket.start()
            #add to connections
            self.connections.append(server_socket)
            print('Ready to receive messages from ', conn.getpeername())

    #broadcast method
    def broadcast(self, message, source):
        for connection in self.connections:
            if connection.sockname != source:
                connection.send(message)
    
    def remove_connection(self, connection):
        self.connections.remove(connection)

class ServerSocket(threading.Thread):
    
    def __init__(self, conn, sockname, server):
        super().__init__()
        self.conn = conn
        self.sockname = sockname
        self.server = server
    
    def run(self):
        while True:
            try:
                message = self.conn.recv(1024)
                message = message.decode('ascii')
            except:
                break
            if message:
                print('{} : {!r}'.format(self.sockname, message))
                self.server.broadcast(message, self.sockname)
            else:
                print('{} has left the chat'.format(self.sockname))
                self.conn.close()
                server.remove_connection(self.server)
                return
    
    def send(self, message):
        self.conn.sendall(message.encode('ascii'))   
    
def exit(server):
    while True:
        msg = input('')
        if msg == 'quit':
            print('Closing connections...')
            for connection in server.connections:
                print('...')
                connection.conn.close()
            print('Shutting down server...')
            os._exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', metavar='IP-ADDR', type=str, default="0.0.0.0", help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port')
    args = parser.parse_args()

    server = Server(args.host, args.p)
    server.start()

    exit = threading.Thread(target = exit, args = (server,))
    exit.start()
