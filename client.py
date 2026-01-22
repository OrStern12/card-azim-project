import argparse
import sys
from connection import Connection
from card import Card


def add_cardaz_argument(parser: argparse.ArgumentParser, word: str): #function to add each arg of the cardaz to the parser
    parser.add_argument(word, type=str, help="the " + word + " of the cardaz") 


def get_args() -> (
    argparse.Namespace
):  # this function received the arguments at the beggining (ip, port of the server)
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    cardaz_arg_list = ["name", "creator", "path", "riddle", "solution"] #list of the args we need for the cardaz
    for arg in cardaz_arg_list:
        add_cardaz_argument(parser, arg)
    return parser.parse_args()


def main():
    args = get_args()
    
    try:
        client = Connection.connect(args.server_ip, args.server_port)
        cardaz = Card.create_from_path(   #creating card for arguments
            args.name, args.creator, args.path, args.riddle, args.solution
        ) 
        cardaz.cryptimage.encrypt("super secret key") #encrypting the image
        message = cardaz.serialize() 
        client.send_message(message)
        client.close()
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
