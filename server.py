import argparse
import threading
from listener import Listener
from connection import Connection
from card import Card
import sys


def manage_connection(c: Connection):  # function to manage a single connection
    serialized_cardaz = c.receive_message()
    cardaz = Card.deserialize(serialized_cardaz) #creating a cardaz according to the bytes sent
    print(cardaz)
    c.close()


def get_args() -> (
    argparse.Namespace
):  # this function deals with the argument received in the beggining
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    return parser.parse_args()

def main():
    args = get_args()
    server = Listener(args.server_ip, args.server_port)
    while True:
        connection = server.accept()
        thr = threading.Thread(
            target=manage_connection, args=(connection,), kwargs={}
        )  # thread handeling
        thr.start()

if __name__ == "__main__":
    sys.exit(main())

