from utilities.error_handler import ResponseCode
from pymongo import MongoClient
from typing import Optional
from abstract_record import mongo_safe

class ChecksumDAO:
    def __init__(self, client: MongoClient, database_name: str):
        self.__db = client[database_name]
        self.__collection = self.__db["checksum"]

    @mongo_safe
    def get_checksum(self, file_name: str) -> Optional[ResponseCode]:
        document = self.__collection.find_one({"fileName": file_name})
        return document
    
    #If you would like to change the checksum of a particular file, consider changing it manually in the database