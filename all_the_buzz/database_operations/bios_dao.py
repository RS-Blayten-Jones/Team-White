from abstract_record import DatabaseAccessObject

class PublicBioDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("bios_public", client_uri, database_name)

class PrivateBioDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("bios_private", client_uri, database_name)