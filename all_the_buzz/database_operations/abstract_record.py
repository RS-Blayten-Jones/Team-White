from pymongo import MongoClient
from abc import ABC
from typing import Any, Optional, Callable
from pymongo.errors import PyMongoError
from functools import wraps
from utilities.logger import LoggerFactory
from utilities.error_handler import ResponseCode
from entities.credentials_entity import Credentials

'''
abstract_record.py

This module is provides the superclass for all DAO objects. Most of the functions here are generalized

Functions:
    -mongo_safe <decorator>: ensures that any exception will be caught or result and will be encapsulated
    by a ResponseCode
    -rbac_action <decorator>: determines which roles have access to a function based on ROLE_MATRIX table
    -prepare_entry <override>: used before create to insert default values in DB 
    -get_by_key: returns ResponseCode with entry if found
    -get_by_fields: returns ResponseCode with list of entries if any
    -get_all_records: returns all records in a table with an optional limit to the number returned
    -get_random: returns ResponseCode with list of entries (defined by user's number request);
    if too many are requested, an error is returned
    -get_short_record: returns ResponseCode with list of entries (defined by user) less than desired
    number of characters; if too many are requested, an error is returned
    -update_record: updates table and then returns success and the number updated (find by ID only)
    -create_record: creates new record and then returns ID if successful. 201 response code
    -delete_record: deletes a record by ID and returns success
    -delete_record_by_field: deletes records by field. Exactly one (no more, no less) field used
'''

def mongo_safe(func):
    '''
    Wraps a function to ensure that a ResponseCode is always returned and that the result of a given
    function is added to data.
    
    Args:
        func: base function to be wrapped

    Returns:
        wrapper: a wrapper that will return a ResponseCode with the error or result of the passed
        in function
    '''
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
    ROLE_MATRIX = {
        "read": ["Employee", "Manager"],
        "create": ["Employee", "Manager"],
        "update": ["Employee", "Manager"],
        "delete": ["Employee", "Manager"]
    }

    def __init__(self, table_name: str, client: MongoClient, database_name: str, credentials: Credentials):
        self.__db = client[database_name]
        self.__collection = self.__db[table_name]
        self.__logger = LoggerFactory.get_general_logger()
        self.__credentials = credentials

    #Checks the current credential's role against the ROLE_MATRIX which holds compatible roles with a given action
    @staticmethod
    def rbac_action(action: str):
        '''
        Wraps a function to ensure that a ResponseCode is always returned and that the result of a given
        function is added to data.
        
        Args:
            func: base function to be wrapped

        Returns:
            wrapper: a wrapper that will return a ResponseCode with the error or result of the passed
            in function
        '''
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                allowed_roles = self.ROLE_MATRIX.get(action, [])
                if self.__credentials.title not in allowed_roles:
                    return ResponseCode("PermissionIncongruency", f"{self.__credentials.title} not allowed to {action}")
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    #Hook method; this should set any default field values; just override it
    def _prepare_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        return entry  #Default: no changes

    @rbac_action("read")
    def get_by_key(self, ID: str) -> ResponseCode:
        self.__logger.debug(f"Getting {self.__class__.__name__} record by ID {ID}.")
        document = self.__collection.find_one({"_id": ID})
        if document is None:
            return ResponseCode(error_tag="ResourceNotFound")
        return document

    @rbac_action("read")
    def get_by_fields(self, filter: dict[str, Any]) -> ResponseCode:
        self.__logger.debug(f"Getting {self.__class__.__name__} record by fields {filter}.")
        document_list = list(self.__collection.find(filter))
        return document_list
    
    @rbac_action("read")
    def get_all_records(self, limit: int = None) -> ResponseCode:
        self.__logger.debug(f"Getting all {self.__class__.__name__} records with limit {limit}.")
        cursor = self.__collection.find({})
        if limit is not None:
            cursor = cursor.limit(limit)
        documents = list(cursor)
        if not documents:
            return ResponseCode(error_tag="ResourceNotFound")
        return documents
    
    @rbac_action("read")
    def get_random(self, numReturned: int, filter: dict[str, Any] = None) -> ResponseCode:
        filter = filter or {}
        self.__logger.debug(f"Getting {numReturned} random {self.__class__.__name__} record by fields {filter}.")
        random_documents = list(self.__collection.aggregate([
            {"$match": filter},
            {"$sample": {"size": numReturned}}
        ]))
        if len(random_documents) < numReturned:
            self.__logger.warning(f"Requested {numReturned}, but only returned {len(random_documents)} records.")
        return random_documents
    
    @rbac_action("read")
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
        if len(result) < numReturned:
            self.__logger.warning(f"Requested {numReturned}, but only returned {len(result)} records.")
        return result

    @rbac_action("update")
    @mongo_safe
    def update_record(self, ID: str, updates: dict[str, Any]) -> ResponseCode:
        if not updates:
            return ResponseCode("MalformedContent", "Update payload must not be empty.")
        self.__logger.debug(f"Updating {self.__class__.__name__} with ID {ID}: {updates}.")
        update_op = {"$set": updates}
        result = self.__collection.update_one({"_id": ID}, update_op)
        if result.matched_count == 0:
            return ResponseCode(error_tag="ResourceNotFound")
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    
    @rbac_action("create")
    @mongo_safe
    def create_record(self, entry: dict[str, Any]) -> ResponseCode:
        entry = self._prepare_entry(entry) #Determines if there should be default field values; override in subclass
        self.__logger.debug(f"Creating {self.__class__.__name__} record: {entry}.")
        result = self.__collection.insert_one(entry)
        self.__logger.debug(f"Created! New ID {result.inserted_id}")
        return ResponseCode("PostSuccess", result) #May need to edit this if we want to send 203 for pending. TODO: ask Kassidy

    @rbac_action("delete")
    @mongo_safe
    def delete_record(self, ID: str) -> ResponseCode:
        self.__logger.debug(f"Deleting {self.__class__.__name__} record.")
        result = self.__collection.delete_one({"_id": ID})
        if result.deleted_count == 0:
            return ResponseCode(error_tag="ResourceNotFound")
        return {"deleted_count": result.deleted_count}
    
    @rbac_action("delete")
    @mongo_safe
    def delete_record_by_field(self, filter: dict[str: Any]) -> ResponseCode:
        if not filter:
            return ResponseCode("MalformedContent", "Delete filter must not be empty.")
        if len(filter) > 1:
            return ResponseCode("MalformedContent", "Delete filter must contain only one field.")
        self.__logger.debug(f"Deleting {self.__class__.__name__} record by filter {filter}.")
        result = self.__collection.delete_many(filter)
        return {"deleted_count": result.deleted_count}