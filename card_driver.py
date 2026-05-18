from card import *
import os
import json
from abc import ABC, abstractmethod
class CardDriver(ABC):
    @abstractmethod
    def __init__(self):
        self.creator_list = []
    def save(self,  card: Card, dir_path: Union[str, PathLike] = '.'):
        self.creator_list.append(card.name)

    def get_identifier(self, card: Card):
        return (card.name,card.creator)

    def load (self, identifier: str):
        pass
    
    def get_creators(self):
        return self.creator_list
    
    def get_creator_cards(self, creator: str):
        pass





    