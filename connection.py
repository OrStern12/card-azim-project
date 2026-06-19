from __future__ import annotations
import socket

MAX_RECV_TIME = 20
PACKAGE_SIZE = 16384

class Connection:
    def __init__(self, connection: socket.socket): #initialize connection with socket
        connection.settimeout(MAX_RECV_TIME)
        self.connection = connection

    def __repr__(self) -> str: # print who the connection is from and to who
        client = self.connection.getsockname()
        server = self.connection.getpeername()
        return f"connection from {client[0]} : {client[1]} to {server[0]} : {server[1]}" #in index 0 we have the ip, and in index 1 we have the port number
    
    def send_message(self, message: bytes): #sends message through socket
        self.connection.send(message)
    
    def receive_message(self) -> bytes: #receives message through socket
        try:
            data = b""
            while True:
                packet = self.connection.recv(PACKAGE_SIZE) #recieve 16KB each iteration until the end
                if not packet:
                    break
                data+=packet
            return data
        except socket.timeout:
            raise socket.timeout("communication failure")

    @classmethod
    def connect(cls, host, port) -> Connection: # creates a new connection to the given host and port
        new_socket = socket.socket()
        new_socket.connect((host, port))
        new_conn = Connection(new_socket)
        return new_conn
    
    def close(self): #closes communication
        self.connection.close()

    def __enter__(self) -> Connection:
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
