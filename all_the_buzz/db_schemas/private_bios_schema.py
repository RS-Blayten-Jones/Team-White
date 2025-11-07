# Copyright (C) 2025 Team White 
# Licensed under the MIT License
# See LICENSE for more details

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl
import os
from dotenv import load_dotenv

# stuff for the secret file and the database URI
load_dotenv() 
ATLAS_URI = os.getenv("ATLAS_URI")
DATABASE_NAME = "team_white_database"
COLLECTION_NAME = "bios_private"

#this is an example of creating a database connection and is just an example, keep it commented out
# try:
#     client = MongoClient(ATLAS_URI, server_api=ServerApi('1'))
#     db = client[DATABASE_NAME]
#     print("MongoDB client initialized successfully.")

# except Exception as e:
#     print(f"An error occurred during connection or command execution: {e}")


#the mongo db schema with the validation criteria
bios_private_schema = {
    # $and forces all rules in the array to be true
    "$and": [
        #RULE 1: Basic Structure Validation $jsonSchema
        #validates types, enums, the ALWAYS required fields, and nested structures
        {
            "$jsonSchema": {
                "bsonType": "object",
                #original_id and explanation are NOT in the required list here, they are conditionally handled below.
                "required": ["_id", "is_edit", "name", "paragraph", "language" ,"source_url"], #ADD THE OG ID FIELD 
                "properties": {
                    "_id": {"bsonType": "objectId"},
                    "is_edit": {"bsonType": "bool"},
                    "original_id": {"bsonType": "objectId"},
                    "birth_year": {"bsonType": "int"},
                    "death_year": {"bsonType": "int"},
                    "name": {"bsonType": "string"},
                    "paragraph": {"bsonType": "string"},
                    "summary": {"bsonType": "string"},
                    "source_url": {"bsonType": "string"}, 
                    "language": {"bsonType": "string"},

                    # Nested content structure ensures all possible fields are defined
                    
                }
            }
        },

        #RULE 2: Conditional Check: is_edit=True REQUIRES original_id
        {
            "$or": [
                { "is_edit": False },
                { "$and": [ 
                    { "is_edit": True },
                    { "original_id": { "$exists": True, "$ne": None } }
                ]}
            ]
        },

        #RULE 3: Conditional Check: level=3 REQUIRES explanation
        

        #RULE 4: Conditional Check: Content Structure for QA vs. One Liner
        
    ]
}

#This code underneath is code that is only run once to create a collection with the schema above ^^
# try:
#     client = MongoClient(ATLAS_URI, server_api=ServerApi('1'))
#     db = client[DATABASE_NAME]
#     if COLLECTION_NAME in db.list_collection_names(): #this should not be the case but just to be safe
#         print(f"Updating validation rules for existing collection: {COLLECTION_NAME}...")
#         db.command('collMod', COLLECTION_NAME, **{'validator': bios_private_schema, 'validationLevel': 'strict'})
#         print("Validation rules updated successfully (validationLevel: strict).")
#     else:
#         print(f"Creating collection with validation rules: {COLLECTION_NAME}...")
#         db.create_collection(
#             COLLECTION_NAME, 
#             validator=bios_private_schema, #****change this line to say collection_privateOrPublic_schema
#             validationAction='error',
#             validationLevel='strict'
#         )
#         print("Collection created with validation successfully.")




# This(below) was me practicing putting an invalid document into the database to 
# test it but the code above has to be commented out to run the file again

# invalid_doc = {"is_edit": False, "level": 3, "content": {"type": "one_liner", "text": "A joke"}, "language": "English"}
# try:
#     db[COLLECTION_NAME].insert_one(invalid_doc)
#     print("\nAttempted to insert valid document. SUCCESS.")
# except Exception as e:
#     print(f"Error Message Snippet: {e.details.get('errmsg', 'Validation Error')}")


# except Exception as e:
#     print(f"An error occurred during connection or command execution: {e}")

# finally:
#     if 'client' in locals() and client is not None:
#         client.close()