import socket

MAX_RECV_TIME = 20

class Connection:
    def __init__(self, connection: socket.socket): #initialize connection with socket
        connection.settimeout(MAX_RECV_TIME)
        self.connection = connection

    def __repr__(self): # print who the connection is from and to who
        client = self.connection.getsockname()
        server = self.connection.getpeername()
        return "connection from " + (str)(client[0]) + ":" + (str)(client[1]) + " to " + (str)(server[0]) + ":" + (str)(server[1]) #in index 0 we have the ip, and in index 1 we have the port number
    
    def send_message(self, message: bytes): #sends message through socket
        self.connection.send(message)
    
    def receive_message(self): #receives message through socket
        try:
            return self.connection.recv(1024).decode()
        except socket.timeout:
            print("communication failure")

    @classmethod
    def connect(cls, host, port): # creates a new connection to the given host and port
        new_socket = socket.socket()
        new_socket.connect((host, port))
        new_conn = Connection(new_socket)
        return new_conn
    
    def close(self): #closes communication
        self.connection.close()

    def __enter__(self):
        return self
    
    def __exit__(self):
        self.close()
