import argparse
import sys
import socket
server = socket.socket()

def run_server():
    c, address = server.accept()
    print(c.recv(1024).decode())
    
def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()

args = get_args()
server.bind((args.server_ip, args.server_port))
server.listen(10)
while True:
    run_server()
