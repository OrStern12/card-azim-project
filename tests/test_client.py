from card import Card
import socket
import client
import sys
import unittest

class MockSocket:
    sent_data = b''
    addr = None
    def settimeout(self, num: int):
        pass
    def connect(self, addr):
        MockSocket.addr = addr
    def send(self, data: bytes):
        MockSocket.sent_data = data
    def recv(self):
        return MockSocket.sent_data
    def close(self):
        pass

def test_client_main_1(monkeypatch):
    monkeypatch.setattr(socket, 'socket', MockSocket)
    test_args = [
        "client.py",
        "127.0.0.1", 
        "2000", 
        "name",
        "or",
        r"C:\Users\user\Documents\card-azim-project\pic1.PNG", 
        "2+2", 
        "4"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)
    client.main()
    card1 = Card.deserialize(MockSocket().recv())
    card2 = Card.create_from_path("name", "or", r"C:\Users\user\Documents\card-azim-project\pic1.PNG", "2+2", "4")
    assert card1.solution != card2.solution
    card1.solution = "4"
    card2.cryptimage.encrypt("super secret key")
    assert Card.serialize(card1) == Card.serialize(card2)
    assert card2.cryptimage.decrypt("super secret key")

def test_client_main_2(monkeypatch):
    monkeypatch.setattr(socket, 'socket', MockSocket)
    test_args = [
        "client.py",
        "127.0.0.1", 
        "2000", 
        "name",
        "or",
        r"C:\Users\user\Documents\card-azim-project\pic1.PNG", 
        "2+2", 
        "4"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)
    client.main()
    card1 = Card.deserialize(MockSocket().recv())
    card2 = Card.create_from_path("name", "or", r"C:\Users\user\Documents\card-azim-project\pic2.PNG", "2+2", "4")
    assert card1.solution != card2.solution
    card1.solution = "4"
    card2.cryptimage.encrypt("super secret key")
    assert Card.serialize(card1) != Card.serialize(card2)
    assert not card2.cryptimage.decrypt("wrong secret key")
    assert card1.riddle == card2.riddle
    