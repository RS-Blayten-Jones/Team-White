from pymongo import MongoClient
from abc import ABC
from typing import Any, Optional
from pymongo.errors import PyMongoError
from functools import wraps
from utilities.logger import LoggerFactory
from utilities.error_handler import ResponseCode

def mongo_safe(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> ResponseCode:
        try:
            result = func(*args, **kwargs)
            return ResponseCode("TODO: CHANGE THIS", result)
        except PyMongoError as e:
            error_tag = e.__class__.__name__
            return ResponseCode(error_tag=error_tag)
    return wrapper

class DatabaseAccessObject(ABC):
    def __init__(self, table_name: str, client: MongoClient, database_name: str):
        self.__db = client[database_name]
        self.__collection = self.__db[table_name]
        self.__logger = LoggerFactory.get_general_logger()

    #Hook method; this should set any default field values; just override it
    def _prepare_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        return entry  #Default: no changes

    @mongo_safe
    def get_by_key(self, ID: str) -> ResponseCode:
        self.__logger.debug(f"Getting {self.__class__.__name__} record by ID {ID}.")
        document = self.__collection.find_one({"_id": ID})
        return document

    @mongo_safe
    def get_by_fields(self, filter: dict[str, Any]) -> ResponseCode:
        self.__logger.debug(f"Getting {self.__class__.__name__} record by fields {filter}.")
        document_list = list(self.__collection.find(filter))
        return document_list
    
    @mongo_safe
    def get_random(self, numReturned: int, filter: dict[str, Any] = None) -> ResponseCode:
        filter = filter or {}
        self.__logger.debug(f"Getting {numReturned} random {self.__class__.__name__} record by fields {filter}.")
        random_document = list(self.__collection.aggregate([
            {"$match": filter},
            {"$sample": {"size": numReturned}}
        ]))
        return random_document
    
    @mongo_safe
    def get_short_record(self, numReturned: int, filter: dict[str, Any] = None, max_length: int = 80) -> ResponseCode:
        filter = filter or {}
        self.__logger.debug(f"Getting  {numReturned} random short (less than {max_length} characters) {self.__class__.__name__} record by fields {filter}.")
        #randomizes the result, because I guess it does not matter?
        pipeline = [
        {
            "$match": {
                "$and": [
                    filter,
                    {
                        #return only files whose content is less than max_length
                        "$expr": {
                            "$lt": [{ "$strLenCP": "$content" }, max_length]
                        }
                    }
                ]
            }
        },
        { "$sample": { "size": numReturned } }
        ]
        result = list(self.__collection.aggregate(pipeline))
        return result

    @mongo_safe
    def update_record(self, ID: str, updates: dict[str, Any]) -> ResponseCode:
        self.__logger.debug(f"Updating {self.__class__.__name__} with ID {ID}: {updates}.")
        update_op = {"$set": updates}
        result = self.__collection.update_one({"_id": ID}, update_op)
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    
    @mongo_safe
    def create_record(self, entry: dict[str, Any]) -> ResponseCode:
        entry = self._prepare_entry(entry) #Determines if there should be default field values; override in subclass
        self.__logger.debug(f"Creating {self.__class__.__name__} record: {entry}.")
        result = self.__collection.insert_one(entry)
        self.__logger.debug(f"Created! New ID {result.inserted_id}")
        return result.inserted_id

    @mongo_safe
    def delete_record(self, ID: str) -> ResponseCode:
        self.__logger.debug(f"Deleting {self.__class__.__name__} record.")
        result = self.__collection.delete_one({"_id": ID})
        return {"deleted_count": result.deleted_count}
    
class DAOFactory:
    #Factory for DAO to ensure only one instance per sub-class exists
    #This allows for dependency injection without the drawbacks of a global Singleton object
    #Below are example usages of this class to manipulate individual DAOs
    '''
    #Create a DAO
    public_joke_dao = DAOFactory.create_dao(\"PublicJokeDAO\", uri, db_name)

    #Get the same DAO later
    same_dao = DAOFactory.get_dao(\"PublicJokeDAO\")

    #Reset just one DAO
    DAOFactory.reset(\"PublicJokeDAO\")

    #Or reset all
    DAOFactory.reset()
    '''

    _instances: dict[type, DatabaseAccessObject] = {}

    @classmethod
    def create_dao(cls, dao_class: str, client_uri: str, database_name: str) -> DatabaseAccessObject:
        if dao_class in cls._instances:
            raise RuntimeError(f"{dao_class.__name__} instance already created. Use get_dao() to access it.")
        instance = dao_class(client_uri, database_name)
        cls._instances[dao_class] = instance
        return instance

    @classmethod
    def get_dao(cls, dao_class: str) -> DatabaseAccessObject:
        if dao_class not in cls._instances:
            raise RuntimeError(f"{dao_class.__name__} instance not yet created. Use create_dao() first.")
        return cls._instances[dao_class]

    @classmethod
    def set_dao(cls, dao_class:str, instance: DatabaseAccessObject):
        cls._instances[dao_class] = instance

    @classmethod
    def reset(cls, dao_class: Optional[str] = None):
        if dao_class:
            cls._instances.pop(dao_class, None)
        else:
            cls._instances.clear()