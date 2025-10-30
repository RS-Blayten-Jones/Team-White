from pymongo import MongoClient
from abc import ABC
from typing import Any
from pymongo.errors import PyMongoError
from functools import wraps
from utilities.logger import LoggerFactory
from utilities.error_handler import ResponseCode

def mongo_safe(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> ResponseCode:
        try:
            result = func(*args, **kwargs)
            if isinstance(result, ResponseCode):
                return result  #Don't wrap again
            return ResponseCode("GeneralSuccess", result)
        except PyMongoError as e:
            error_tag = e.__class__.__name__
            return ResponseCode(error_tag=error_tag)
        except Exception as e:
            error_tag = e.__class__.__name__
            data = f"UnhandledError: {error_tag}"
            return ResponseCode(error_tag=error_tag, data=data)
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
        if document is None:
            return ResponseCode(error_tag="ResourceNotFound")
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
        random_documents = list(self.__collection.aggregate([
            {"$match": filter},
            {"$sample": {"size": numReturned}}
        ]))
        return random_documents
    
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
        if result.matched_count == 0:
            return ResponseCode(error_tag="ResourceNotFound")
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    
    @mongo_safe
    def create_record(self, entry: dict[str, Any]) -> ResponseCode:
        entry = self._prepare_entry(entry) #Determines if there should be default field values; override in subclass
        self.__logger.debug(f"Creating {self.__class__.__name__} record: {entry}.")
        result = self.__collection.insert_one(entry)
        self.__logger.debug(f"Created! New ID {result.inserted_id}")
        return ResponseCode("PostSuccess", result) #May need to edit this if we want to send 203 for pending. TODO: ask Kassidy

    @mongo_safe
    def delete_record(self, ID: str) -> ResponseCode:
        self.__logger.debug(f"Deleting {self.__class__.__name__} record.")
        result = self.__collection.delete_one({"_id": ID})
        if result.deleted_count == 0:
            return ResponseCode(error_tag="ResourceNotFound")
        return {"deleted_count": result.deleted_count}