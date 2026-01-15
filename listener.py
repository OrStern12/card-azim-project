import socket
from connection import Connection

MAX_RECV_TIME = 20

class Listener:

    def __repr__(self): #prints description of listener
        return "Listener(port=" + (str)(self.port) + "), host=" + (str)(self.host) + "), backlog=" + (str)(self.backlog) + ")"
    
    def start(self): #starts to listen
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)
    
    def stop(self): # stops listening and closes the port
        self.socket.close()

    def accept(self): # waits for connection and accepts
        c, address = self.socket.accept()
        return Connection(c)

    def __init__(self, host: str, port: int, backlog: int = 1000): # initializes the listener and starts to listen
        self.host = host
        self.port = port
        self.backlog = backlog
        self.socket = socket.socket()
        self.start()
    
    def __enter__(self):
        return self
    
    def __exit__(self):
        self.stop()


