from card import Card
import socket
import client
import sys
import os
import pytest

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

subdir = r"C:\Users\user\card-azim-project"
code_file = "client.py"
server = "127.0.0.1"
port = "2000"
name = "name"
creator = "or"
file_name = os.path.join(subdir, r"pic1.PNG")
riddle = "2+2"
solution = "4"

@pytest.fixture
def create_psuedo_client(monkeypatch):
    monkeypatch.setattr(socket, 'socket', MockSocket)
    test_args = [
        code_file,
        server, 
        port, 
        name,
        creator,
        file_name, 
        riddle, 
        solution
    ]
    monkeypatch.setattr(sys, 'argv', test_args)
    client.main()

def test_client_main_1(create_psuedo_client):
    '''This test checks: solution is not serialized, card remains the same after being serialized and deserialized, and encrypt/decrypt work'''
    deserialized_card = Card.deserialize(MockSocket().recv())
    created_by_path_card = Card.create_from_path("name", "or", file_name , "2+2", "4")
    assert deserialized_card.solution != created_by_path_card.solution
    deserialized_card.solution = "4"
    created_by_path_card.cryptimage.encrypt("super secret key")
    assert Card.serialize(deserialized_card) == Card.serialize(created_by_path_card)
    assert created_by_path_card.cryptimage.decrypt("super secret key")
    created_by_path_card.cryptimage.encrypt("wrong secret key")
    assert Card.serialize(deserialized_card) != Card.serialize(created_by_path_card)

def test_client_main_2(create_psuedo_client):
    '''chekcs that different picks are not equal in serialize, that serealize/deserilize keep riddle the same, and that decrypting does not work with wrong key'''
    deserialized_card = Card.deserialize(MockSocket().recv())
    created_by_path_card = Card.create_from_path("name", "or", os.path.join(subdir, r"pic2.PNG"), "2+2", "4")
    deserialized_card.solution = "4"
    created_by_path_card.cryptimage.encrypt("super secret key")
    assert Card.serialize(deserialized_card) != Card.serialize(created_by_path_card) 
    assert not created_by_path_card.cryptimage.decrypt("wrong secret key")
    assert deserialized_card.riddle == created_by_path_card.riddle
    