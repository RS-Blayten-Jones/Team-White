from abstract_record import DatabaseAccessObject, mongo_safe
from utilities.error_handler import ResponseCode
from typing import Any
from datetime import date

class PublicQuoteDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("quotes_public", client_uri, database_name)

    #used_status should default to false when added!
    def _prepare_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        entry["used_status"] = False
        return entry
    
    @mongo_safe
    def _reset_quotes(self) -> ResponseCode:
        self.__logger.debug(f"Reseting all quotes...")
        result = self.__collection.update_many({}, {"$set": {"used_status": False}})
        return result
    
    @mongo_safe
    def get_quote_of_day(self) -> ResponseCode:
        #Check to see if there are any unused quotes
        num_unused_quotes = self.__collection.count_documents({"used_status": False})
        today = date.today()
        #If it is a new year OR all of the quotes have been used, reset and get total number of quotes
        if((today.month == 1 and today.day == 1) or (num_unused_quotes == 0)):
            self._reset_quotes()
            num_unused_quotes = self.__collection.count_documents({"used_status": False})
        #Knuth multiplication method; reduced to 32 bit hash-space; spreads out values well
        #Unique value for each day...
        seed = 10000*today.year + 100*today.month + today.day
        hashed = (seed * 2654435761) % 2**32
        unused_list = list(self.__collection.find({"used_status": False}))
        #Obtain a record using a hashed value so that it is unified across users and not random per session
        record = unused_list[hashed % num_unused_quotes]
        self._update_as_used(record["_id"])
        return record
    
    @mongo_safe
    def _update_as_used(self, ID):
        #Ensure that this quote has been used so that it is not used again until it has been reset
        self.update_record(ID, {"used_status": True})


class PrivateQuoteDAO(DatabaseAccessObject):
    def __init__(self, client_uri: str, database_name: str):
        super().__init__("quotes_private", client_uri, database_name)

    #used_status should default to false when added!    
    def _prepare_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        entry["used_status"] = False
        return entry