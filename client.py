#!/usr/bin/env python3
#code mainly sourced and adapted from first tutorial link

import threading
import socket
import argparse
import os
import sys

class Send(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        
        while True:
            message = input('{}: '.format(self.name))

            if message == 'quit':
                self.sock.sendall('Server: {} has left the chat'.format(self.name).encode('ascii'))
                break
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))

        print('\nQuitting...')
        self.sock.close()
        os._exit(0)

class Receive(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
    
    def run(self):

        while True:
            message = self.sock.recv(1024)
            if message:
                print('\r{}\n{}: '.format(message.decode('ascii'), self.name), end = '')
            else:
                print('\nConnection lost! Get a better ISP!!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)

class Client:
    
    def __init__(self, name, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
    
    def start(self):
        print('\nTrying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('\nSuccessfully connected to {}:{}'.format(self.host, self.port))
        print('\nWelcome! Thank you for using my chatroom!\n You will appear to other users as {}! Initialising...'.format(self.name))

        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        send.start()
        receive.start()

        self.sock.sendall('Server: {} has joined the chat.'.format(self.name).encode('ascii'))
        print('\rAll set! Type "quit" to leave the chatroom. Enjoy!\n')
        print('{}: '.format(self.name), end='')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('name', help='Name being used by user', default='User')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('port', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)')
    args = parser.parse_args()
    client = Client(args.name, args.host, args.port)
    client.start()