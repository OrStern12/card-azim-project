from __future__ import annotations
from PIL import Image
from crypt_image import Cryptimage
from typing import Union
from os import PathLike

def get_string_from_bytes(data: bytes, index: int) -> tuple[str, int]:
        name_len = int.from_bytes(data[index:index+4], byteorder='big', signed=False)
        index +=4
        name = data[index:index+name_len].decode()
        return name, index+name_len

class Card:
    def __init__(self, name: str, creator: str, cryptimage: Cryptimage, riddle: str, solution: Union[str, None]):
        self.name = name
        self.creator = creator
        self.cryptimage = cryptimage
        self.riddle = riddle
        self.solution = solution

    def __repr__(self) -> str: #returns string to describe the cardaz
        return "Card name=" + self.name + ", creator=" + self.creator 
    
    def __str__(self) -> str: #returns string to describe the cardaz (slightly different then before)
        return_string = "Card " + self.name + " by " + self.creator + "\nriddle: " + self.riddle + "\nsolution: "
        if self.solution is None:
            return_string += "unsolved"
        else:
            return_string += self.solution
        return return_string
    
    @classmethod
    def create_from_path(cls, name: str, creator: str, path: Union[str, PathLike], riddle: str, solution: str) -> Card:
        cryptimage = Cryptimage.create_from_path(path)
        return cls(name, creator, cryptimage, riddle, solution)
    
    def serialize(self) -> bytes: #returning a bytes object to represent the cardaz
        return_val = b"" #keeps the bytes we need to return, updates for each value needed in the data
        return_val += len(self.name).to_bytes(4, byteorder='big')+self.name.encode() #adding the name and creator
        return_val += len(self.creator).to_bytes(4, byteorder='big')+self.creator.encode()
        return_val += self.cryptimage.image.size[0].to_bytes(4, byteorder='big') #adding length and width of the image
        return_val += self.cryptimage.image.size[1].to_bytes(4, byteorder='big')
        return_val += self.cryptimage.image.tobytes() #adding the image to the bytes
        if self.cryptimage.key_hash: #making sure the key exists
            return_val += self.cryptimage.key_hash 
        else:
            raise Exception("sending unencrypted object") #If the key is None this will happen
        return_val += len(self.riddle).to_bytes(4, byteorder='big')+self.riddle.encode()
        return return_val
        
    
    @classmethod
    def deserialize(cls, data: bytes) -> Card: #receives bytes that represent a cardaz, creates the cardaz and returns it 
        count = 0 #counts where we are in the traversal of the data
        name, count = get_string_from_bytes(data, count) #gets name for cardaz and updates count
        creator, count = get_string_from_bytes(data, count) #gets creator for cardaz and updates count
        width = int.from_bytes(data[count:count+4], byteorder='big', signed=False) #gets width and height of image
        height = int.from_bytes(data[count+4:count+8], byteorder='big', signed=False)
        count = count+8
        image_data = data[count:count+3*width*height] #getting image data. the 3 is because we always use 'RGB'
        image = Image.frombytes('RGB', (width, height), image_data) #creates image from data
        count += 3*width*height
        key = data[count:count+32] #receives hashed key
        crypt_img = Cryptimage(image, key) #creates cryptimage object with the image and key we received
        count+=32
        riddle, count = get_string_from_bytes(data, count) #gets riddle for cardaz and updates count
        solution = None
        return cls(name, creator, crypt_img, riddle, solution) #creates and returns the cardaz based on the data
