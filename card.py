from __future__ import annotations
from PIL import Image
from crypt_image import Cryptimage
from typing import Union
from os import PathLike

def img_bytes(card) -> bytes:
    length = card.cryptimage.image.size[0].to_bytes(4, byteorder='big') #adding length and width of the image
    width = card.cryptimage.image.size[1].to_bytes(4, byteorder='big')
    image = card.cryptimage.image.tobytes() #adding the image to the bytes
    if card.cryptimage.key_hash: #always true but needed due to syntax
        key_hash = card.cryptimage.key_hash 
    else:
        raise UnencryptedException("sending unencrypted object") #If the key is None this will happen
    return length + width + image + key_hash

class UnencryptedException(Exception):
    """Exception raised for sending unencrypted object"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"

def get_string_from_bytes(data: bytes, index: int) -> tuple[str, int]:
        """The function turns 4 bytes from a bytes object at a certain index to a string"""
        name_len = int.from_bytes(data[index:index+4], byteorder='big', signed=False)
        index +=4
        name = data[index:index+name_len].decode()
        return name, index+name_len

def deserialize_image(count, data):
        """function recieves bytes data and returns image, as well as key and the place in the bytes object where the image ends"""
        width = int.from_bytes(data[count:count+4], byteorder='big', signed=False) #gets width and height of image
        height = int.from_bytes(data[count+4:count+8], byteorder='big', signed=False)
        count = count+8
        image_data = data[count:count+3*width*height] #getting image data. the 3 is because we always use 'RGB'
        image = Image.frombytes('RGB', (width, height), image_data) #creates image from data
        count += 3*width*height
        key = data[count:count+32] #receives hashed key
        count+=32
        return image, count, key

class Card:
    def __init__(self, name: str, creator: str, cryptimage: Cryptimage, riddle: str, solution: Union[str, None] = None):
        self.name = name
        self.creator = creator
        self.cryptimage = cryptimage
        self.riddle = riddle
        self.solution = solution

    def __repr__(self) -> str: 
        """returns string to describe the cardaz"""
        return "Card name=" + self.name + ", creator=" + self.creator 
    
    def __str__(self) -> str: 
        """returns string to describe the cardaz (slightly different then before)"""
        return_string = "Card " + self.name + " by " + self.creator + "\nriddle: " + self.riddle + "\nsolution: "
        if self.solution is None:
            return_string += "unsolved"
        else:
            return_string += self.solution
        return return_string
    
    @classmethod
    def create_from_path(cls, name: str, creator: str, path: Union[str, PathLike], riddle: str, solution:  Union[str, None]) -> Card:
        cryptimage = Cryptimage.create_from_path(path)
        return cls(name, creator, cryptimage, riddle, solution)
    
    def serialize(self) -> bytes: 
        '''returning a bytes object to represent the cardaz'''
        return_val = b"" #keeps the bytes we need to return, updates for each value needed in the data
        name = len(self.name).to_bytes(4, byteorder='big')+self.name.encode() #adding the name and creator
        creator = len(self.creator).to_bytes(4, byteorder='big')+self.creator.encode()
        image_path = len((str)(self.cryptimage.path)).to_bytes(4, byteorder='big')+(str)(self.cryptimage.path).encode()
        riddle = len(self.riddle).to_bytes(4, byteorder='big')+self.riddle.encode()
        return name + creator + img_bytes(self) + image_path + riddle
        
    
    @classmethod
    def deserialize(cls, data: bytes) -> Card: 
        '''receives bytes that represent a cardaz, creates the cardaz and returns it'''
        count = 0 #counts where we are in the traversal of the data
        name, count = get_string_from_bytes(data, count) #gets name for cardaz and updates count
        creator, count = get_string_from_bytes(data, count) #gets creator for cardaz and updates count
        image, count, key = deserialize_image(count, data)
        path, count = get_string_from_bytes(data, count)
        crypt_img = Cryptimage(image, key, path) #creates cryptimage object with the image and key we received
        riddle, count = get_string_from_bytes(data, count) #gets riddle for cardaz and updates count
        return cls(name, creator, crypt_img, riddle) #creates and returns the cardaz based on the data