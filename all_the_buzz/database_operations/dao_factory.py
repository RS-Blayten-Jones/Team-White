from database_operations.abstract_record import DatabaseAccessObject
from database_operations.bios_dao import PublicBioDAO, PrivateBioDAO
from database_operations.jokes_dao import PublicJokeDAO, PrivateJokeDAO
from database_operations.quotes_dao import PublicQuoteDAO, PrivateQuoteDAO
from database_operations.trivia_dao import PublicTriviaDAO, PrivateTriviaDAO
from typing import Optional, Union
from pymongo import MongoClient

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
    def create_dao(cls, dao_class_name: str, client: MongoClient, database_name: str) -> Union[DatabaseAccessObject]:
        #If the given type has not been registered, throw an error by testing for None type; else, check for instances
        dao_class = _DAO_REGISTRY.get(dao_class_name, "Error")
        if(not dao_class):
            raise RuntimeError(f"This DAO type has not been registered. Try a valid identifier.")
        if dao_class in cls._instances:
            raise RuntimeError(f"{dao_class.__name__} instance already created. Use get_dao() to access it.")
        instance = dao_class(client, database_name)
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