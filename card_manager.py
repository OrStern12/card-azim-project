from card import *
import os
import json

class CardManager:
    def save(self,  card: Card, dir_path: Union[str, PathLike] = '.'):
        directory_name = f"{dir_path}\\{self.get_identifier(card)}"
        os.mkdir(directory_name)
        directory_name+="\\metadata.json"
        image_file_name = f"{self.get_identifier(card)}"+".jpg"
        card.cryptimage.image.save(image_file_name)
        json_file = json.dumps({
            "name": card.name,
            "creator" : card.creator,
            "riddle" : card.riddle,
            "solution" : card.solution,
            "image_path" : card.cryptimage.path,
            "image" : image_file_name
        })
        with open(directory_name, "w") as file:
            file.write(json_file)

    def get_identifier(self, card: Card):
        return card.name+"_"+card.creator

    def load (self, identifier: str):
        file_name = f"C:/Users/user/{identifier}/metadata.json"
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
        cryimage = Cryptimage.create_from_path(data["image_path"])
        return Card(data['name'], data['creator'], cryimage, data['riddle'], data['solution'])


    