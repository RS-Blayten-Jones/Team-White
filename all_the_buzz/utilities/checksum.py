#!!!!!!!!!!!!!!!!!
#WORK IN PROGRESS
#!!!!!!!!!!!!!!!!!


from all_the_buzz.database_operations.checksum_dao import ChecksumDAO
from pymongo import MongoClient
import os
import hashlib

def compute_sha256(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

#Insert the files that you want to checksum.
#When listing files, use the relative path location compared to the all_the_buzz folder
file_list = {"database_operations/dao_factory.py", "server.py", "utilities/authentication.py", "utilities/checksum.py", "utilities/sanitize.py"}

#Set up the DAO for the checksum table
uri = ""
db_name = ""
client = MongoClient(uri)
dao = ChecksumDAO(client, db_name)

for file in file_list:
    full_path = os.path.join("all_the_buzz", file)
    file_name = os.path.basename(file)
    hash_value = compute_sha256(full_path)

    record = dao.get_checksum(file_name)
    if(hash_value != record["hash_value"]):
        pass