# Copyright (C) 2025 Team White 
# Licensed under the MIT License
# See LICENSE for more details

from all_the_buzz.utilities.error_handler import ResponseCode
from pymongo import MongoClient
from all_the_buzz.database_operations.abstract_record import mongo_safe

class ChecksumDAO:
    '''
    Despite being a DAO, this class does not extend from the DatabaseAccessObject class for security reasons.
    This class establishes a connection to the checksum collection, which should not be accessed by users or
    managers. This is entirely for the computer to confirm file integrity
    '''
    def __init__(self, client: MongoClient, database_name: str):
        '''
        Args:
            client (MongoClient): the client that connects the DAO to the database
            database_name (str): the name of the actual database that all of the collections are held in
        '''
        self.__db = client[database_name]
        self.__collection = self.__db["checksum"]

    @mongo_safe
    def get_checksum(self, file_name: str) -> ResponseCode:
        '''
        Return checksum given a file_name 
        
        Args:
            file_name (str): the file_name of the file you would like to confirm the checksum of

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode
            with the checksum as a string as data
        '''
        document = self.__collection.find_one({"fileName": file_name})
        checksum = document["hash_value"]
        return checksum
    
    #If you would like to change the checksum of a particular file, consider changing it manually in the database