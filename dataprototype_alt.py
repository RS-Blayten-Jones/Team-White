from pymongo import MongoClient

from abc import ABC, abstractmethod
from typing import Optional, Any
from enum import Enum
from pymongo.errors import PyMongoError
from functools import wraps
from dataclasses import dataclass
from LogTest.code.logger_factory import LoggerFactory

@dataclass
class ResponseCode:
    success: bool
    error_code: int
    error_tag: str
    message: str
    data: Optional[Any] = None



ERROR_CODE_MAP = {
    #PyMongo Errors
    "AutoReconnect": (503, "The operation MAY have succeeded, but the connection to the database was lost. Please retry."),
    "BulkWriteError": (400, "The write operation failed due to invalid data."),
    "CollectionInvalid": (422, "The submitted data does not meet the collection's validation rules"),
    "ConfigurationError": (500, "Database configuration error. Please contact support."),
    "ConnectionFailure": (503, "Unable to connect to the database. Please try again later."),
    "CursorNotFound": (410, "The requested data stream is no longer available."),
    "DocumentTooLarge": (413, "The document is too large to be stored. Please reduce its size or wait for more storage space to be added to the server."),
    "DuplicateKeyError": (409, "A record with this identifier already exists."),
    "EncryptedCollectionError": (422, "Could not create encrypted collection due to invalid configuration."),
    "EncryptionError": (500, "Data encryption failed. Please try again or contact support."),
    "ExecutionTimeout": (504, "The database query took too long and was aborted. Please try again at a later time."),
    "InvalidName": (400, "Invalid collection or database name used in the request."),
    "InvalidOperation": (400, "The requested operation is not allowed in this context."),
    "InvalidURI": (400, "Invalid database connection string. Check your URI format."),
    "NetworkTimeout": (504, "Database operation timed out. The result may be incomplete. Please try again at a later time."),
    "NotPrimaryError": (503, "Database is temporarily unavailable due to server maintenance."),
    "OperationFailure": (500, "The database operation failed. Please check your request and try again."),
    "ProtocolError": (502, "Unexpected response from the database. Please try again."),
    "RefuseToBrew": (418, "Server refused to brew; provide tea instead of coffee or retry with brewer."),
    "ServerSelectionTimeoutError": (503, "Database server is currently unavailable. Please retry shortly."),
    "WTimeoutError": (504, "The write operation did not meet replication requirements in time."),
    "WaitQueueTimeoutError": (503, "Database is busy. Please wait and try again."),
    "WriteConcernError": (500, "The write was successful but did not meet durability requirements."),
    "WriteError": (400, "The write operation failed due to invalid data."),
    "PyMongoError": (500, "An unexpected and unknown database error occurred. Please try again or contact support."),
    
    #Custom Error Calls
        #Token Validation Errors
    "AuthorizationTimeout": (503, "Authorization server did not respond. Try again later."),
    "MalformedAuthorizationResponse": (502, "Authorization server gave a malformed object to the API. Try again later."),
    "UnauthorizedToken": (401, "Token was expired or invalid. Please send a new valid JWT."),
        #API Request Errors
    "MalformedContent": (400, "Request content had malformed syntax. Please check your request."),
    "RateLimit": (429, "Too many requests have been sent. Please wait until you can request again."),
        #Security Errors
    "ChecksumValidationError": (500, "Integrity check failed. Try again later."),
    "FieldValidationError": (400, "One of the fields was of an incorrect type. Please ensure that data is of the correct field type."),
    "LengthValidationError": (413, "One of the fields was too large. Please ensure that data is within acceptable parameters."),
    "PermissionIncongruency": (403, "User does not have the correction permissions required for this action."),
}



def mongo_safe(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> ResponseCode:
        logger = LoggerFactory.get_general_logger()
        try:
            result = func(*args, **kwargs)
            logger.info(f"Success! Data: {result}")
            return ResponseCode(success=True, error_code=200, error_tag="OK", message="Success!", data=result)
        except PyMongoError as e:
            error_tag = e.__class__.__name__
            #Defualt to 500 error if it cannot be found in look-up table
            error_code, message = ERROR_CODE_MAP.get(error_tag, (500, "An unexpected error occurred."))
            logger.error(f"{error_code}. {error_tag}: {message}; data: {result}")
            return ResponseCode(success=False, error_code=error_code, error_tag=error_tag, message=message, data=result)
    return wrapper



class DatabaseAccessObject(ABC):
    def __init__(self, table_name: str, client_uri: str, database_name: str):
        self.__client = MongoClient(client_uri)
        self.__db = self.__client[database_name]
        self.__collection = self.__db[table_name]
        self.__logger = LoggerFactory.get_general_logger()

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
    def get_short_content(self, numReturned: int, filter: dict[str, Any] = None, max_length: int = 80) -> ResponseCode:
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
        self.__logger.debug(f"Creating {self.__class__.__name__} record: {entry}.")
        result = self.__collection.insert_one(entry)
        self.__logger.debug(f"Created! New ID {result.inserted_id}")
        return result.inserted_id

    @mongo_safe
    def delete_record(self, ID: str) -> ResponseCode:
        self.__logger.debug(f"Deleting {self.__class__.__name__} record.")
        result = self.__collection.delete_one({"_id": ID})
        return {"deleted_count": result.deleted_count}

class PublicJokeDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("jokes_public", client_uri, database_name)

class PrivateJokeDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("jokes_private", client_uri, database_name)

class PublicBioDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("bios_public", client_uri, database_name)

class PrivateBioDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("bios_private", client_uri, database_name)

class PublicTriviaDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("trivia_public", client_uri, database_name)

class PrivateTriviaDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("trivia_private", client_uri, database_name)

class PublicQuoteDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("quotes_public", client_uri, database_name)

    @mongo_safe
    def check_not_used(self) -> ResponseCode:
        self.__logger.debug(f"Checking for no used quotes...")
        document_list = list(self.__collection.find({"used_status": False}))
        return document_list
    
    @mongo_safe
    def reset_quotes(self) -> ResponseCode:
        self.__logger.debug(f"Reseting all quotes...")
        result = self.__collection.update_many({}, {"$set": { "used_status": True}})
        return result

class PrivateQuoteDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("quotes_private", client_uri, database_name)



class ChecksumDAO:
    def __init__(self, client_uri: str, database_name: str):
        self.__client = MongoClient(client_uri)
        self.__db = self.__client[database_name]
        self.__collection = self.__db["checksum"]

    @mongo_safe
    def get_checksum(self, file_name: str) -> ResponseCode:
        document = self.__collection.find_one({"fileName": file_name})
        return document
    
    #If you would like to change the checksum of a particular file, consider changing it manually in the database
    


class DAOFactory:
    #Factory for DAO to ensure only one instance per sub-class exists
    #This allows for dependency injection without the drawbacks of a global Singleton object
    #Below are example usages of this class to manipulate individual DAOs
    '''
    #Create a DAO
    public_joke_dao = DAOFactory.create_dao(PublicJokeDAO, uri, db_name)

    #Get the same DAO later
    same_dao = DAOFactory.get_dao(PublicJokeDAO)

    #Reset just one DAO
    DAOFactory.reset(PublicJokeDAO)

    #Or reset all
    DAOFactory.reset()
    '''

    _instances: dict[type, DatabaseAccessObject] = {}

    @classmethod
    def create_dao(cls, dao_class: type[DatabaseAccessObject], client_uri: str, database_name: str) -> DatabaseAccessObject:
        if dao_class in cls._instances:
            raise RuntimeError(f"{dao_class.__name__} instance already created. Use get_dao() to access it.")
        instance = dao_class(client_uri, database_name)
        cls._instances[dao_class] = instance
        return instance

    @classmethod
    def get_dao(cls, dao_class: type[DatabaseAccessObject]) -> DatabaseAccessObject:
        if dao_class not in cls._instances:
            raise RuntimeError(f"{dao_class.__name__} instance not yet created. Use create_dao() first.")
        return cls._instances[dao_class]

    @classmethod
    def set_dao(cls, dao_class: type[DatabaseAccessObject], instance: DatabaseAccessObject):
        cls._instances[dao_class] = instance

    @classmethod
    def reset(cls, dao_class: Optional[type[DatabaseAccessObject]] = None):
        if dao_class:
            cls._instances.pop(dao_class, None)
        else:
            cls._instances.clear()