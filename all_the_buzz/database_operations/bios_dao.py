from abstract_record import DatabaseAccessObject
from utilities.error_handler import ResponseCode
from typing import Optional

class PublicBioDAO(DatabaseAccessObject):
    ROLE_MATRIX = {
        "read": ["Employee", "Manager"],
        "create": ["Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }

    def __init__(self, client_uri: str, database_name: str):
        super().__init__("bios_public", client_uri, database_name)

class PrivateBioDAO(DatabaseAccessObject):
    ROLE_MATRIX = {
        "read": ["Manager"],
        "create": ["Employee", "Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }

    def __init__(self, client_uri: str, database_name: str):
        super().__init__("bios_private", client_uri, database_name)