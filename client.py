import argparse
import sys
from connection import Connection

def get_args(): # this function received the arguments at the beggining (ip, port of the server)
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("data", type=str, help="the data")
    return parser.parse_args()


def main():
    args = get_args()
    try:
        client = Connection.connect(args.server_ip, args.server_port)

        client.send_message(args.data.encode())
        client.close()
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
