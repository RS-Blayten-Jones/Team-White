from all_the_buzz.database_operations.abstract_record import DatabaseAccessObject, mongo_safe
from all_the_buzz.utilities.error_handler import ResponseCode
from typing import Any
from datetime import date
from pymongo import MongoClient

class PublicQuoteDAO(DatabaseAccessObject):
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
        super().__init__("quotes_public", client, database_name)

    #used_status should default to none when added!
    def _prepare_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        entry["used_status"] = "None"
        return entry
    
    @mongo_safe
    def _reset_quotes(self) -> ResponseCode:
        '''
        Sets all quotes "used_status" to "None"

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the 
            UpdateResult object
        '''
        self.__logger.debug(f"Reseting all quotes...")
        result = self.__collection.update_many({}, {"$set": {"used_status": "None"}})
        return result
    
    @DatabaseAccessObject.rbac_action("read")
    @mongo_safe
    def get_quote_of_day(self) -> ResponseCode:
        '''
        Gets the quote of the day using today's date. After that date is used, it is marked. On New Year's
        all of the quotes are unmarked back to being "unused"

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the 
            JSON document
        '''
        #Check to see if there are any unused quotes
        num_unused_quotes = self.__collection.count_documents({"used_status": "None"})
        today = date.today()
        today_string = today.strftime("%m/%d/%Y")
        existing_record = self.__collection.find({"used_status": today_string})
        #if there is a quote being used for today, just return that one
        if(existing_record is not None):
            return existing_record
        #If it is a new year OR all of the quotes have been used, reset and get total number of quotes
        if((today.month == 1 and today.day == 1) or (num_unused_quotes == 0)):
            self._reset_quotes()
            num_unused_quotes = self.__collection.count_documents({"used_status": "None"})
        #Knuth multiplication method; reduced to 32 bit hash-space; spreads out values well
        #Unique value for each day...
        seed = 10000*today.year + 100*today.month + today.day
        hashed = (seed * 2654435761) % 2**32
        unused_list = list(self.__collection.find({"used_status": "None"}))
        #Obtain a record using a hashed value so that it is unified across users and not random per session
        record = unused_list[hashed % num_unused_quotes]
        self.update_record(record["_id"], {"used_status": today_string})
        return record
    
class PrivateQuoteDAO(DatabaseAccessObject):
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
        super().__init__("quotes_private", client, database_name)

    #used_status should default to none when added!    
    def _prepare_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        entry["used_status"] = "None"
        return entry