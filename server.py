import argparse
import threading
from listener import Listener
from connection import Connection
from card import Card
from driver import Driver
from saver import CardSaver, card_id
import sys
import time
import os

manager = CardSaver()
working_dir = r"C:\Users\user"

def signal_pause(server):
    '''checks if exit signals is received and pauses the program if so'''
    try:
        while(True):
            time.sleep(0.1)
            user_input = input()
            if(user_input == "exit"):
                print("\nRecieved exit signal.")
                break
    except:
        print("error occured")
    finally:
        server.stop()
    
def recieve_cardaz_from_connection(c: Connection): 
    """ function to manage a single connection and receive a cardaz"""
    try:
        serialized_cardaz = c.receive_message()
        print("received card")
        cardaz = Card.deserialize(serialized_cardaz) #creating a cardaz according to the bytes sent
        manager.save(cardaz, )
        print(f"Saved card to sql database")
    except:
        print("connection error")
    finally:
        c.close()


def get_args() -> (
    argparse.Namespace
):  
    """ this function deals with the argument received in the beggining """
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    return parser.parse_args()

def main():
    args = get_args()
    server = Listener(args.server_ip, args.server_port)
    thr2 = threading.Thread(
            target=signal_pause, args=(server, ), kwargs={}
        )  # thread handeling
    thr2.start()
    while True:
        try:
            connection = server.accept()
            thr = threading.Thread(
                target=recieve_cardaz_from_connection, args=(connection,), kwargs={}
            )
            thr.start()
        except:
            server.stop()
            break
        
if __name__ == "__main__":
    sys.exit(main())

