from abstract_record import DatabaseAccessObject

class PublicTriviaDAO(DatabaseAccessObject):
    ROLE_MATRIX = {
        "read": ["Employee", "Manager"],
        "create": ["Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }

    def __init__(self, client_uri: str, database_name: str):
        super().__init__("trivia_public", client_uri, database_name)

class PrivateTriviaDAO(DatabaseAccessObject):
    ROLE_MATRIX = {
        "read": ["Manager"],
        "create": ["Employee", "Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }

    def __init__(self, client_uri: str, database_name: str):
        super().__init__("trivia_private", client_uri, database_name)