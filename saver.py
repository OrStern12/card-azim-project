import sqlite3
import mysql.connector
from mysql.connector import Error
from card import *
import os
import json
from card_driver import CardDriver
from abc import ABC, abstractmethod
from os import getenv
from dotenv import load_dotenv
from mssql_python import connect


import pyodbc  



# Use 'yes' and explicitly define the driver
connection_string = (
    r"Driver={ODBC Driver 17 for SQL Server};"
    r"Server=localhost\MSSQLSERVER02;"
    r"Database=TestDB;"
    r"Trusted_Connection=yes;"
    r"autocommit=True;"
)


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
        conn.autocommit = True
        cursor = conn.cursor()
        image_bytes = img_bytes(card)
        self.creator_list.append(card.creator)
        cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[{card.creator}]') AND type in (N'U')) "
               f"BEGIN CREATE TABLE [dbo].[{card.creator}] (name NVARCHAR(255), riddle NVARCHAR(255), solution NVARCHAR(255), path NVARCHAR(255), image_bin VARBINARY(MAX)) END;") #create table for creator of none exists
        imagepath = card.cryptimage.path if card.cryptimage else None
        creator_name = card.creator.strip()
        sql = f"INSERT INTO [dbo].[{creator_name}] (name, riddle, solution, path, image_bin) VALUES (?, ?, ?, ?, ?)"
        cursor.setinputsizes([
            (pyodbc.SQL_WVARCHAR, 255),
            (pyodbc.SQL_WVARCHAR, 255), 
            (pyodbc.SQL_WVARCHAR, 255), 
            (pyodbc.SQL_WVARCHAR, 255),  
            (pyodbc.SQL_LONGVARBINARY,)    # image_bin, need to inform of large binary string
        ])
        val = (card.name, card.riddle, card.solution, imagepath, image_bytes)
        cursor.execute(sql, val) #insert now column
        cursor.close()
        conn.close()
        
    def get_identifier(self, card: Card) -> tuple:
        return (card.name,card.creator)

    def load (self, identifier: tuple) -> Card:
        load_dotenv()
        conn = pyodbc.connect(connection_string)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT name, riddle, solution, path, image_bin FROM [dbo].[{identifier[0]}];")
        for tup in cursor.fetchall():
            if tup[0] == identifier[1]:
                image, a, key = deserialize_image(0, tup[4]) #tup[4] contains the image string
                cryimage = Cryptimage(image, key, tup[4])
                cursor.close()
                conn.close()
                return Card(tup[0], identifier[0], cryimage, tup[1], tup[2])
    
    def get_creators(self) -> list:
        return self.creator_list
    
    def get_creator_cards(self, creator: str) -> list:
        load_dotenv()
        conn = pyodbc.connect(connection_string)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT name, riddle, solution, path, image_bin FROM [dbo].[{creator}];")
        card_list=[]
        for tup in cursor.fetchall():  #passing through the table of the creator
            image, a, key = deserialize_image(0, tup[4])
            cryimage = Cryptimage(image, key, tup[4])
            card_list.append(Card(tup[0], creator, cryimage, tup[1], tup[2]))
        cursor.close()
        conn.close()
        return card_list
    
    


