from __future__ import annotations
from PIL import Image
import hashlib
from Crypto.Cipher import AES
from typing import Union
from os import PathLike

class Cryptimage:
    def __init__(self, image: Image.Image, key: Union[bytes, None]):
        self.image = image
        self.key_hash = key

    @classmethod
    def create_from_path(cls, path: Union[str, PathLike]) -> Cryptimage:
        if not isinstance(path, str):
            path = path.__fspath__() #Making sure the path is a string
        image = Image.open(path)
        image = image.convert('RGB') #Making sure the image is RGB as we want
        new_crypt_image = cls(image, None) #Using initiate to create a new Cryptimage
        return new_crypt_image
    
    def encrypt (self, key: str): #the function we create a hashed key by using haslib on the received key twice, and use the hashed key to enctypt the image
        bin_key = key.encode("utf-8")
        self.key_hash = hashlib.sha256(hashlib.sha256(bin_key).digest()).digest() #hashing the key as needed
        width, height = self.image.size  
        mode = self.image.mode
        bin_image = (self.image.tobytes())
        cipher = AES.new(bin_key, AES.MODE_EAX, nonce=b'arazim') #creating the encryption cipher
        encrypted_bin_image = cipher.encrypt(bin_image) #encrypting the bytes of the image
        encrypted_image = Image.frombytes(mode, (width, height), encrypted_bin_image)
        self.image = encrypted_image
    
    def decrypt (self, key: str) -> bool: #the function will check if the received key the correct base key, and if so, decrypt the image
        bin_key = key.encode()
        if self.key_hash != hashlib.sha256(hashlib.sha256(bin_key).digest()).digest(): #checking if the received key is equal to the base key (before it was hashed)
            return False
        width, height = self.image.size
        mode = self.image.mode
        bin_image = (self.image.tobytes())
        cipher = AES.new(bin_key, AES.MODE_EAX, nonce=b'arazim') #creating cipher
        decrypted_bin_image = cipher.decrypt(bin_image) #decrypting bytes of image
        decrypted_image = Image.frombytes(mode, (width, height), decrypted_bin_image)
        self.image = decrypted_image
        return True