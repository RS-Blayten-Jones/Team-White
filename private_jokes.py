from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl

ATLAS_URI = "mongodb+srv://***********:*********@clusterteamwhite.tgh3kdu.mongodb.net/?appName=ClusterTeamWhite"
DATABASE_NAME = "team_white_database"
COLLECTION_NAME = "jokes_private"

jokes_private_schema = {
    # $and forces all rules in the array to be true
    "$and": [
        #RULE 1: Basic Structure Validation $jsonSchema
        #validates types, enums, the ALWAYS required fields, and nested structures
        {
            "$jsonSchema": {
                "bsonType": "object",
                #original_id and explanation are NOT in the required list here, they are conditionally handled below.
                "required": ["_id", "is_edit", "level", "content", "language"],
                "properties": {
                    "_id": {"bsonType": "objectId"},
                    "is_edit": {"bsonType": "bool"},
                    "original_id": {"bsonType": "objectId"},
                    "level": {"bsonType": "int", "enum": [1, 2, 3]},
                    "explanation": {"bsonType": "string"},
                    "language": {"bsonType": "string"},

                    # Nested content structure ensures all possible fields are defined
                    "content": {
                        "bsonType": "object",
                        "required": ["type"],
                        "properties": {
                            "type": {"bsonType": "string", "enum": ["one_liner", "qa"]},
                            "text": {"bsonType": "string"},
                            "question": {"bsonType": "string"},
                            "answer": {"bsonType": "string"}
                        }
                    }
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
        {
            "$or": [
                { "$and": [
                    { "level": { "$in": [1, 2] } }, # Valid if level is 1 or 2
                ]},
                { "$and": [
                    { "level": 3 },                 # OR Valid if level is 3 AND
                    { "explanation": { "$exists": True, "$ne": None } } #
                ]}
            ]
        },

        #RULE 4: Conditional Check: Content Structure for QA vs. One Liner
        {
            "$or": [
                # CASE A: If type is 'qa', then 'question' and 'answer' MUST exist
                { "$and": [
                    { "content.type": "qa" },
                    { "content.question": { "$exists": True, "$ne": None } },
                    { "content.answer": { "$exists": True, "$ne": None } },
                ]},
                # CASE B: If type is 'one_liner', then 'text' MUST exist
                { "$and": [
                    { "content.type": "one_liner" },
                    { "content.text": { "$exists": True, "$ne": None } }
                ]}
            ]
        }
    ]
}

#Do not run this code again, it is just example code 
# try:
#     db = client[DATABASE_NAME]
    
#     if COLLECTION_NAME in db.list_collection_names():
#         # 2. If it exists, use run_command to update the validation rules
#         print(f"Updating validation rules for existing collection: {COLLECTION_NAME}...")
        
#         db.command('collMod', COLLECTION_NAME, **{'validator': jokes_private_schema, 'validationLevel': 'strict'})
        
#         print("Validation rules updated successfully (validationLevel: strict).")

#     else:
#         # 3. If it doesn't exist, create it with the validation rules
#         print(f"Creating collection with validation rules: {COLLECTION_NAME}...")
        
#         db.create_collection(
#             COLLECTION_NAME, 
#             validator=jokes_private_schema, 
#             validationAction='error',
#             validationLevel='strict'
#         )
        
#         print("Collection created with validation successfully.")

#     valid_doc = {"is_edit": False, "level": 1, "content": {"type": "one_liner", "text": "A joke"}, "language": "English"}
#     try:
#         db[COLLECTION_NAME].insert_one(valid_doc)
#         print("\nAttempted to insert valid document. SUCCESS.")
#     except Exception as e:
#         print(f"Error Message Snippet: {e.details.get('errmsg', 'Validation Error')}")


# except Exception as e:
#     print(f"An error occurred during connection or command execution: {e}")

# finally:
#     if 'client' in locals() and client is not None:
#         client.close()