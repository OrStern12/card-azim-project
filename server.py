import argparse
import sys
import socket
PORT = 22222
IP = '127.0.0.1'
server = socket.socket()

def run_server():
    c, address = server.accept()
    print(c.recv(1024).decode())
    
def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('client_ip', type=str,
                        help='the client\'s ip')
    parser.add_argument('client_port', type=int,
                        help='the client\'s port')
    return parser.parse_args()

args = get_args()
server.bind((args.client_ip, args.client_port))
server.listen(5)
while True:
    run_server()