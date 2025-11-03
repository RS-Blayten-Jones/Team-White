from pymongo import MongoClient
from bson.objectid import ObjectId
from abc import ABC
from typing import Any, Callable
from pymongo.errors import PyMongoError
from functools import wraps
from utilities.logger import LoggerFactory
from utilities.error_handler import ResponseCode
from entities.credentials_entity import Credentials

def mongo_safe(func):
    '''
    Wraps a function to ensure that a ResponseCode is always returned and that the result of a given
    function is added to data.
    
    Args:
        func (Any): base function to be wrapped

    Returns:
        wrapper (function): a wrapper that will return a ResponseCode with the error or result of the passed
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
    '''
    This class is an abstract class that all DAO objects extend from to access their corresponding collections.
    Each extension can define a custom ROLE_MATRIX for role-based acessed control.
    '''
    ROLE_MATRIX = {
        "read": ["Employee", "Manager"],
        "create": ["Employee", "Manager"],
        "update": ["Employee", "Manager"],
        "delete": ["Employee", "Manager"]
    }

    def __init__(self, table_name: str, client: MongoClient, database_name: str):
        '''
        Args:
            table_name (str): the name of the collection that the DAO accesses
            client (MongoClient): the client that connects the DAO to the database
            database_name (str): the name of the actual database that all of the collections are held in
        '''
        self.__db = client[database_name]
        self.__collection = self.__db[table_name]
        self.__logger = LoggerFactory.get_general_logger()
        self.__credentials = None

    #Checks the current credential's role against the ROLE_MATRIX which holds compatible roles with a given action
    @staticmethod
    def rbac_action(action: str):
        '''
        Wraps a function to ensure that it can be called with the current credential's permissions
        
        Args:
            action (str): which action to check in the ROLE_MATRIX with the credential's title
            func (Callable): base function to be wrapped

        Returns:
            decorator (function(?)): a decorator that will return a ResponseCode with the error or result of the passed
            in function or not even run the function if the ROLE_MATRIX does not give permission
        '''
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                allowed_roles = self.ROLE_MATRIX.get(action, [])
                if(self.__credentials is None):
                    return ResponseCode("PermissionIncongruency", f"No Credentials were provided.")
                if self.__credentials.title not in allowed_roles:
                    return ResponseCode("PermissionIncongruency", f"{self.__credentials.title} not allowed to {action}")
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    #Hook method; this should set any default field values; just override it
    def _prepare_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        '''
        Hooks to a function and overrides to give default values for MongoDB documents
        
        Args:
            entry (dict[str, Any]): the entry to be processed

        Returns:
            entry (dict[str, Any]): the entry after processing (usually defining a default field)
        '''
        return entry  #Default: no changes
    
    def set_credentials(self, credentials: Credentials) -> None:
        '''
        Sets the current credentials of the DAO
        
        Args:
            credentials (Credentials): the credentials given by the authorization server to use for role-based access control
        '''
        self.__credentials = credentials

    def clear_credentials(self) -> None:
        '''
        Clears any set credentials by setting the current one t "None"
        '''
        self.__credentials = None

    @rbac_action("read")
    def get_by_key(self, ID: str) -> ResponseCode:
        '''
        Return MongoDB document by ID
        
        Args:
            ID (str): a string corresponding to a MongoDB _id value

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode
            with the JSON document as data
        '''
        self.__logger.debug(f"Getting {self.__class__.__name__} record by ID {ID}.")
        document = self.__collection.find_one({"_id": ObjectId(ID)})
        if document is None:
            return ResponseCode(error_tag="ResourceNotFound")
        return document

    @rbac_action("read")
    def get_by_fields(self, filter: dict[str, Any]) -> ResponseCode:
        '''
        Return MongoDB documents by given fields
        
        Args:
            filter (dict[str, Any]): a dictionary corresponding to the fields to check and the values by which to filter

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the JSON
            documents as data
        '''
        self.__logger.debug(f"Getting {self.__class__.__name__} record by fields {filter}.")
        document_list = list(self.__collection.find(filter))
        return document_list
    
    @rbac_action("read")
    def get_all_records(self, limit: int = None) -> ResponseCode:
        '''
        Return all (or the first x) MongoDB documents from a collection
        
        Args:
            limit (int optional): an integer that determines the number of records to send back. By default, it is set to None and returns the entire set of documents

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the JSON
            documents from the collection as data
        '''
        self.__logger.debug(f"Getting all {self.__class__.__name__} records with limit {limit}.")
        cursor = self.__collection.find({})
        if limit is not None:
            cursor = cursor.limit(limit)
        documents = list(cursor)
        if not documents:
            return ResponseCode(error_tag="ResourceNotFound")
        return documents
    
    @rbac_action("read")
    def get_random(self, numReturned: int = 1, filter: dict[str, Any] = None) -> ResponseCode:
        '''
        Return a set number of random records given an optional filter
        
        Args:
            numReturned (int optional): an integer that determines the number of documents returned. Defaults to 1
            filter (dict[str, Any] optional): a dictionary corresponding to the fields to check and the values by which to filter

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the JSON documents as data
        '''
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
        '''
        Return a set number of random records given an optional filter that also have a content less than
        the given max_length
        
        Args:
            numReturned (int optional): an integer that determines the number of documents returned. Defaults to 1
            filter (dict[str, Any] optional): a dictionary corresponding to the fields to check and the values by which to filter
            max_length (int optional): an integer that determines the max_length of the content field. Defaults to 80

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the JSON documents as data
        '''
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
        '''
        Updates a record of a given ID with given updates
        
        Args:
            ID (str): a string corresponding to a MongoDB _id value
            updates (dict[str, Any]): a dictionary corresponding to the fields to change and the values to change to

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the
            matched_count and modified_count ({1, 1}) as data
        '''
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
        '''
        Creates a record with the entry data given
        
        Args:
            entry (dict[str, Any]): a dictionary of fields and values to add to the collection

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with InsertOneResult
        '''
        entry = self._prepare_entry(entry) #Determines if there should be default field values; override in subclass
        self.__logger.debug(f"Creating {self.__class__.__name__} record: {entry}.")
        result = self.__collection.insert_one(entry)
        self.__logger.debug(f"Created! New ID {str(result.inserted_id)}")
        return ResponseCode("PostSuccess", result)

    @rbac_action("delete")
    @mongo_safe
    def delete_record(self, ID: str) -> ResponseCode:
        '''
        Deletes a record of a given ID
        
        Args:
            ID (str): a string corresponding to a MongoDB _id value

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the
            deleted_count ({1}) as data
        '''
        self.__logger.debug(f"Deleting {self.__class__.__name__} record.")
        result = self.__collection.delete_one({"_id": ObjectId(ID)})
        if result.deleted_count == 0:
            return ResponseCode(error_tag="ResourceNotFound")
        return {"deleted_count": result.deleted_count}
    
    @rbac_action("delete")
    @mongo_safe
    def delete_record_by_field(self, filter: dict[str, Any]) -> ResponseCode:
        '''
        Deletes a record of a given filter
        
        Args:
            filter (dict[str, Any]): a dictionary corresponding to the field to check and the value by which to filter

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the
            deleted_count as data
        '''
        if not filter:
            return ResponseCode("MalformedContent", "Delete filter must not be empty.")
        if len(filter) > 1:
            return ResponseCode("MalformedContent", "Delete filter must contain only one field.")
        self.__logger.debug(f"Deleting {self.__class__.__name__} record by filter {filter}.")
        result = self.__collection.delete_many(filter)
        return {"deleted_count": result.deleted_count}