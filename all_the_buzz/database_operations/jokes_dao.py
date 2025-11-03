from database_operations.abstract_record import DatabaseAccessObject
from pymongo import MongoClient

class PublicJokeDAO(DatabaseAccessObject):
    ROLE_MATRIX = {
        "read": ["Employee", "Manager"],
        "create": ["Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }

    def __init__(self, client: MongoClient, database_name: str):
        '''
        Args:
            client (MongoClient): the client that connects the DAO to the database
            database_name (str): the name of the actual database that all of the collections are held in
        '''
        super().__init__("jokes_public", client, database_name)

class PrivateJokeDAO(DatabaseAccessObject):
    ROLE_MATRIX = {
        "read": ["Manager"],
        "create": ["Employee", "Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }

    def __init__(self, client: MongoClient, database_name: str):
        '''
        Args:
            client (MongoClient): the client that connects the DAO to the database
            database_name (str): the name of the actual database that all of the collections are held in
        '''
        super().__init__("jokes_private", client, database_name)