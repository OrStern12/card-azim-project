from typing import Union
from os import PathLike
from card import Card
from crypt_image import Cryptimage
import os
import json
from card_driver import CardDriver, card_id

subdir = r"C:\Users\user"

class Driver(CardDriver):
    def __init__(self):
        self.creator_list = []
        
    def save(self,  card: Card, dir_path: Union[str, PathLike] = '.'):
        directory_name = f"{dir_path}/{card.creator}"
        print(directory_name)
        if (not os.path.exists(directory_name)): #checking if directory for creator exists
            os.mkdir(directory_name)
        directory_name += f"/{card.name}"
        os.mkdir(directory_name)
        directory_name+="/metadata.json"
        image_file_name = f"{self.get_identifier(card).creator}"+f"_{self.get_identifier(card).name}"+".jpg"
        card.cryptimage.image.save(image_file_name)
        json_file = json.dumps({ #creating json
            "name": card.name,
            "creator" : card.creator,
            "riddle" : card.riddle,
            "solution" : card.solution,
            "image_path" : card.cryptimage.path,
            "image" : image_file_name
        })
        self.creator_list.append(card.name)
        with open(directory_name, "w") as file:
            file.write(json_file)

    def get_identifier(self, card: Card):
        return card_id(card.name,card.creator)

    def load (self, identifier: card_id):
        file_name = f"C:/Users/user/{identifier.creator}/{identifier.name}/metadata.json"
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
        cryimage = Cryptimage.create_from_path(data["image_path"]) #creating image from path
        return Card(data['name'], data['creator'], cryimage, data['riddle'], data['solution'])
    
    def get_creators(self):
        return self.creator_list
    
    def get_creator_cards(self, creator: str):
        card_list = []
        directory = os.path.join(subdir,f"{creator}")
        x= next(os.walk(directory)) #going through the directory
        for name in x[1]:
            file_name = f"{x[0]}/{name}/metadata.json"
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
            cryimage = Cryptimage.create_from_path(data["image_path"])
            card_list.append(Card(data['name'], data['creator'], cryimage, data['riddle'], data['solution']))
        return card_list
    


