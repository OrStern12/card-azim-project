from typing import Union
from os import PathLike
from crypt_image import Cryptimage
from card import Card, deserialize_image, img_bytes
from card_driver import CardDriver, card_id
from dotenv import load_dotenv
import pyodbc  
from collections import namedtuple

connection_string = (
    r"Driver={ODBC Driver 17 for SQL Server};"
    r"Server=localhost\MSSQLSERVER02;"
    r"Database=TestDB;"
    r"Trusted_Connection=yes;"
    r"autocommit=True;"
)
SIZE_OF_CHAR = 255
card_tup = namedtuple('card_tup', ['creator', 'name', 'riddle', 'solution', 'path', 'image_bin'])


def img_bytes(card) -> bytes:
    image_bytes = card.cryptimage.image.size[0].to_bytes(4, byteorder='big') #adding length and width of the image
    image_bytes += card.cryptimage.image.size[1].to_bytes(4, byteorder='big')
    image_bytes += card.cryptimage.image.tobytes() #adding the image to the bytes
    if card.cryptimage.key_hash: #always true but needed due to syntax
        image_bytes += card.cryptimage.key_hash 
    return image_bytes




class CardSaver(CardDriver):
    def __init__(self):
        self.creator_list = []

    def save(self,  card: Card, dir_path: Union[str, PathLike] = '.') -> None:
        load_dotenv()
        conn = pyodbc.connect(connection_string) #opening connection to database
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[card_table]') AND type in (N'U')) "
                f"BEGIN CREATE TABLE [dbo].[card_table] (creator NVARCHAR(255), name NVARCHAR(255), riddle NVARCHAR(255), solution NVARCHAR(255), path NVARCHAR(255), image_bin VARBINARY(MAX)) END;") #create table if none exists
        try:
            image_bytes = img_bytes(card)
            self.creator_list.append(card.creator)
            imagepath = card.cryptimage.path if card.cryptimage else None
            creator_name = card.creator.strip()
            sql = f"INSERT INTO [dbo].[card_table] (creator, name, riddle, solution, path, image_bin) VALUES (?, ?, ?, ?, ?, ?)"
            size_requirment = (pyodbc.SQL_WVARCHAR, SIZE_OF_CHAR)
            cursor.setinputsizes([
                size_requirment,
                size_requirment,
                size_requirment, 
                size_requirment, 
                size_requirment,  
                (pyodbc.SQL_LONGVARBINARY,)    # image_bin, need to inform of large binary string
            ])
            val = (card.creator, card.name, card.riddle, card.solution, imagepath, image_bytes)
            cursor.execute(sql, val) #insert now column
        except:
            print("sql error")
        finally:
            cursor.close()
            conn.close()
        
    def get_identifier(self, card: Card) -> card_id:
        return card_id(card.name,card.creator)

    def load (self, identifier: card_id) -> Card:
        load_dotenv()
        conn = pyodbc.connect(connection_string)
        conn.autocommit = True
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT creator, name, riddle, solution, path, image_bin FROM [dbo].[card_table];")
            for tup in cursor.fetchall():
                tup = card_tup(*tup)
                if tup.creator == identifier.creator and tup.name == identifier.name:
                    image, a, key = deserialize_image(0, tup.image_bin) #tup[4] contains the image string
                    cryimage = Cryptimage(image, key, tup.image_bin)
                    cursor.close()
                    conn.close()
                    return Card(tup.name, identifier.creator, cryimage, tup.riddle, tup.solution)
        except:
            print("sql error")
            cursor.close()
            conn.close()
    
    
    def get_creators(self) -> list:
        return self.creator_list
    
    def get_creator_cards(self, creator: str) -> list:
        load_dotenv()
        conn = pyodbc.connect(connection_string)
        conn.autocommit = True
        cursor = conn.cursor()
        card_list = []
        try:
            cursor.execute(f"SELECT creator, name, riddle, solution, path, image_bin FROM [dbo].[card_table];")
            for tup in cursor.fetchall():
                tup = card_tup(*tup)
                if tup.creator == creator:
                    image, a, key = deserialize_image(0, tup.image_bin) #tup[4] contains the image string
                    cryimage = Cryptimage(image, key, tup.image_bin)
                    card_list.append(Card(tup.name, creator, cryimage, tup.riddle, tup.solution))
        except:
            print("sql error")
        finally:
            cursor.close()
            conn.close()
            return card_list

    
    


