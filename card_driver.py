from card import *
import os
import json
from abc import ABC, abstractmethod
from collections import namedtuple

card_id = namedtuple('card_id', ['name', 'creator'])
class CardDriver(ABC):
    @abstractmethod
    def __init__(self):
        self.creator_list = []

    @abstractmethod
    def save(self,  card: Card, dir_path: Union[str, PathLike] = '.'):
        self.creator_list.append(card.name)

    @abstractmethod
    def get_identifier(self, card: Card):
        return card_id(card.name,card.creator)

    @abstractmethod
    def load (self, identifier: str):
        pass
    
    @abstractmethod
    def get_creators(self):
        return self.creator_list
    
    @abstractmethod
    def get_creator_cards(self, creator: str):
        pass





    