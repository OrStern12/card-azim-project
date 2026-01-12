import argparse
import socket
import threading

server = socket.socket()

def manage_client(c: socket.socket):   #function to manage a single client
    print(c.recv(1024).decode())
    c.close()
    
def get_args():  # this function deals with the argument received in the beggining
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    return parser.parse_args()


args = get_args()
server.bind((args.server_ip, args.server_port))
server.listen(10)
while True:
    c, address = server.accept()
    thr = threading.Thread(target=manage_client, args=(c,), kwargs={}) #thread handeling
    thr.start()
    
