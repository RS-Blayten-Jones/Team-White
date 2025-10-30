from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl
import os
from dotenv import load_dotenv

# stuff for the secret file and the database URI
load_dotenv() 
ATLAS_URI = os.getenv("ATLAS_URI")
DATABASE_NAME = "team_white_database"
COLLECTION_NAME = "jokes_public"

#this is an example of creating a database connection and is just an example, keep it commented out
try:
    client = MongoClient(ATLAS_URI, server_api=ServerApi('1'))
    db = client[DATABASE_NAME]
    print("MongoDB client initialized successfully.")

except Exception as e:
    print(f"An error occurred during connection or command execution: {e}")


#the mongo db schema with the validation criteria
jokes_public_schema = {
    # $and forces all rules in the array to be true
    "$and": [
        #RULE 1: Basic Structure Validation $jsonSchema
        #validates types, enums, the ALWAYS required fields, and nested structures
        {
            "$jsonSchema": {
                "bsonType": "object",
                #original_id and explanation are NOT in the required list here, they are conditionally handled below.
                "required": ["_id", "level", "content", "language"], #ADD THE OG ID FIELD 
                "properties": {
                    "_id": {"bsonType": "objectId"},
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

# #This code underneath is code that is only run once to create a collection with the schema above ^^
# try:
#     client = MongoClient(ATLAS_URI, server_api=ServerApi('1'))
#     db = client[DATABASE_NAME]
#     if COLLECTION_NAME in db.list_collection_names(): #this should not be the case but just to be safe
#         print(f"Updating validation rules for existing collection: {COLLECTION_NAME}...")
#         db.command('collMod', COLLECTION_NAME, **{'validator': jokes_public_schema, 'validationLevel': 'strict'})
#         print("Validation rules updated successfully (validationLevel: strict).")
#     else:
#         print(f"Creating collection with validation rules: {COLLECTION_NAME}...")
#         db.create_collection(
#             COLLECTION_NAME, 
#             validator=jokes_public_schema, #****change this line to say collection_publicOrPublic_schema
#             validationAction='error',
#             validationLevel='strict'
#         )
#         print("Collection created with validation successfully.")




# This(below) was me practicing putting an invalid document into the database to 
# test it but the code above has to be commented out to run the file again

# invalid_doc = {"is_edit": False, "level": 3, "content": {"type": "one_liner", "text": "A joke"}, "language": "English"}
# test_data = [
#   {
#     "level": 5,
#     "language": "english",
#     "content": {
#       "type": "one_liner",
#       "text": "I told my computer I needed a break, and it said 'No problem — I'll crash.'"
#     }
#   },
#   {
#     "level": 3,
#     "language": "spanish",
#     "content": {
#       "type": "qa",
#       "question": "¿Por qué el libro se sintió triste?",
#       "answer": "Porque tenía demasiados problemas."
#     }
#   },
#   {
#     "level": 3,
#     "language": "french",
#     "explanation": "Parce qu'il électron est-il toujours",
#     "content": {
#       "type": "qa",
#       "question": "Pourquoi l'électron est-il toujours en difficulté?"
#     #   "answer": "Parce qu'il est toujours chargé."
#     }
#   },
#   {
#     "level": 8,
#     "language": "english",
#     "explanation": "The humor comes from the unexpected twist in the punchline.",
#     "content": {
#       "type": "one_liner",
#       "text": "I asked the gym instructor if he could teach me to do the splits. He said, 'How flexible are you?' I said, 'I can’t make it on Tuesdays.'"
#     }
#   },
#   {
#     "level": 9,
#     "language": "german",
#     "content": {
#       "type": "qa",
#       "question": "Warum können Geister nicht lügen?",
#       "answer": "Weil man durch sie hindurchsehen kann."
#     }
#   }
# ]
# for i in range(len(test_data)):
#     try:
#         db[COLLECTION_NAME].insert_one(test_data[i])
#         print("\nAttempted to insert valid document. SUCCESS.")
#     except Exception as e:
#         print(f"Error Message Snippet: {e.details.get('errmsg', 'Validation Error')}")


# except Exception as e:
#     print(f"An error occurred during connection or command execution: {e}")

# finally:
#     if 'client' in locals() and client is not None:
#         client.close()