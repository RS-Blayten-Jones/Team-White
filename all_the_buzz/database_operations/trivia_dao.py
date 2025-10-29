from abstract_record import DatabaseAccessObject

class PublicTriviaDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("trivia_public", client_uri, database_name)

class PrivateTriviaDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("trivia_private", client_uri, database_name)