from pymongo import MongoClient

from abc import ABC, abstractmethod
from typing import Optional, Any
from enum import Enum

class DatabaseAccessObject:
    def __init__(self, client_uri: str, database_name: str):
        self.__client_uri = client_uri
        self.__client = MongoClient(client_uri)
        self.__db = self.__client[database_name]

    def get_by_key(self, ID: str, table: type) -> Optional[dict[str, Any]]: 
        collection = self.__db[table.__name__]
        document = collection.find_one({"_id": ID})
        return document

    def get_by_fields(self, table: type, filter: dict[str, Any]) -> list[dict[str, Any]]:
        collection = self.__db[table.__name__]
        document_list = list(collection.find(filter))
        return document_list
    
    def update_record(self, ID: str, table: type, updates: dict[str, Any]) -> bool:
        collection = self.__db[table.__name__]
        update_op = {"$set": updates}
        result = collection.update_one({"_id": ID}, update_op)
        return result.acknowledged
    
    def create_record(self, table: type, entry: dict[str, Any]) -> str:
        collection = self.__db[table.__name__]
        result = collection.insert_one(entry)
        if(result.acknowledged):
            return result.inserted_id
        else:
            return "ERROR"

    def delete_record(self, ID: str, table: type) -> bool:
        collection = self.__db[table.__name__]
        result = collection.delete_one({"_id": ID})
        return result.acknowledged
    

    __client_uri = None
    __client = None
    __db = None

class DAOFactory:
    #Factory for DAO to ensure only one instance exists
    #This allows for dependency injection without the drawbacks of a global Singleton object
    _dao_instance = None

    @classmethod
    def create_dao(cls, client_uri: str, database_name: str) -> DatabaseAccessObject:
        if cls._dao_instance is not None:
            raise RuntimeError("DAO instance already created. Use get_dao() to access it.")
        cls._dao_instance = DatabaseAccessObject(client_uri, database_name)
        return cls._dao_instance

    @classmethod
    def get_dao(cls) -> DatabaseAccessObject:
        if cls._dao_instance is None:
            raise RuntimeError("DAO instance not yet created. Use create_dao() first.")
        return cls._dao_instance
        
    @classmethod
    def set_dao(cls, instance: DatabaseAccessObject):
        cls._dao_instance = instance

    @classmethod
    def reset(cls):
        cls._dao_instance = None

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class ContentObject(ABC):
    def __init__(self, language: str, content: str, ID: None):
        self.__ID = ID
        self.__language = language
        self.__content = content

    #Update these functions to first check for ID    
    def get_document_by_ID(self, DAO: DatabaseAccessObject, ID: int) -> dict[str, Any]:
        return DAO.getByKey(ID, type(self))
    
    def get_document(self, DAO: DatabaseAccessObject, filters: dict[str, Any]) -> list[dict[str, Any]]:
        return DAO.get_by_fields(type(self), filters)
    
    def get_ID(self) -> int:
        return self.__ID
    
    def get_language(self) -> str:
        return self.__language
    
    def get_content(self) -> str:
        return self.__content

class Joke(ContentObject):
    def __init__(self, ID: int, language: str, content: str, difficulty: Difficulty, explanation: str = ""):
        super().__init__(ID, language, content)
        self.__difficulty = difficulty
        self.__explanation = explanation
    
    def get_difficulty(self) -> Difficulty:
        return self.__difficulty
    
    def get_explanation(self) -> str:
        return self.__explanation