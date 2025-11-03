from database_operations.abstract_record import DatabaseAccessObject
from database_operations.bios_dao import PublicBioDAO, PrivateBioDAO
from database_operations.jokes_dao import PublicJokeDAO, PrivateJokeDAO
from database_operations.quotes_dao import PublicQuoteDAO, PrivateQuoteDAO
from database_operations.trivia_dao import PublicTriviaDAO, PrivateTriviaDAO
from utilities.logger import LoggerFactory
from typing import Optional
from pymongo import MongoClient

'''
dao_factory.py

This module allows a singular instance of each DAO to be made without accidentally creating more.

Functions:
    -create_dao <classmethod>: creates a DAO for the specified type and returns it; it will raise an
    error if one exists 
    -get_dao <classmethod>: returns the DAO of a given type if it exists
    -reset <classmethod>: if (for whatever unknown reason???) you need to reset the DAOs, you can clarify
    which one or reset all
'''

_DAO_REGISTRY = {
    "PublicBioDAO": PublicBioDAO,
    "PrivateBioDAO": PrivateBioDAO,
    "PublicJokeDAO": PublicJokeDAO,
    "PrivateJokeDAO": PrivateJokeDAO,
    "PublicQuoteDAO": PublicQuoteDAO,
    "PrivateQuoteDAO": PrivateQuoteDAO,
    "PublicTriviaDAO": PublicTriviaDAO,
    "PrivateTriviaDAO": PrivateTriviaDAO,
    "Error": None
}

class DAOFactory:
    #Factory for DAO to ensure only one instance per sub-class exists
    #This allows for dependency injection without the drawbacks of a global Singleton object
    #Below are example usages of this class to manipulate individual DAOs
    '''
    This class is a factory that creates a single "global" instance of each type of DAO, as long as it is within
    the _DAO_REGISTRY. Cannot be initialized. Use classmethods instead.
    List of acceptable DAO tables:\n
    "PublicBioDAO"\n
    "PrivateBioDAO"\n
    "PublicJokeDAO"\n
    "PrivateJokeDAO"\n
    "PublicQuoteDAO"\n
    "PrivateQuoteDAO"\n
    "PublicTriviaDAO"\n
    "PrivateTriviaDAO"\n
    '''

    _instances: dict[type, DatabaseAccessObject] = {}

    @classmethod
    def create_dao(cls, dao_class_name: str, client: MongoClient, database_name: str) -> DatabaseAccessObject:
        '''
        Creates a DAO of the given class and passes the MongoClient. If one exists, it raises an error
        
        Args:
            dao_class_name (str): a string that represents the table the DAO connects to; must be in the _DAO_REGISTRY
            client (MongoClient): the MongoClient that establishes a connection with the database
            database_name (str): the name of the database where the collection is stored

        Returns:
            instance (DatabaseAccessObject): a DatabaseAccessObject of the given dao_class_name string
        '''
        #If the given type has not been registered, throw an error by testing for None type; else, check for instances
        dao_class = _DAO_REGISTRY.get(dao_class_name, "Error")
        print(f"class: {dao_class}\ninstances: {cls._instances}\n\n")
        if(not dao_class):
            raise RuntimeError(f"This DAO type has not been registered. Try a valid identifier.")
        if dao_class in cls._instances:
            raise RuntimeError(f"{dao_class} instance already created. Use get_dao() to access it.")
        instance = dao_class(client, database_name)
        print(f"Class instance: {instance}")
        cls._instances[dao_class] = instance
        return instance

    @classmethod
    def get_dao(cls, dao_class_name: str) -> DatabaseAccessObject:
        '''
        Returns a DAO if it exists; otherwise, raises an error
        
        Args:
            dao_class_name (str): a string that represents the table the DAO connects to; must be in the _DAO_REGISTRY

        Returns:
            instance (DatabaseAccessObject): a DatabaseAccessObject of the given dao_class_name string
        '''
        if dao_class_name not in cls._instances:
            raise RuntimeError(f"{dao_class_name} instance not yet created. Use create_dao() first.")
        return cls._instances[dao_class_name]

    @classmethod
    def reset(cls, dao_class_name: Optional[str] = None):
        '''
        Resets either a specific DAO (if given a dao_class_name) or all of them
        
        Args:
            dao_class_name (str optional): a string that represents the table the DAO connects to; must be in the _DAO_REGISTRY
        '''
        if dao_class_name:
            cls._instances.pop(dao_class_name, None)
        else:
            cls._instances.clear()
