from abstract_record import DatabaseAccessObject

class PublicJokeDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("jokes_public", client_uri, database_name)

class PrivateJokeDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("jokes_private", client_uri, database_name)