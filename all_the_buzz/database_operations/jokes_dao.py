from abstract_record import DatabaseAccessObject

class PublicJokeDAO(DatabaseAccessObject):
    ROLE_MATRIX = {
        "read": ["Employee", "Manager"],
        "create": ["Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }

    def __init__(self, client_uri: str, database_name: str):
        super().__init__("jokes_public", client_uri, database_name)

class PrivateJokeDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("jokes_private", client_uri, database_name)