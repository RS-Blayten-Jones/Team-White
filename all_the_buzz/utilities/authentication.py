import requests
from utilities.config import config_file_reader
from entities.credentials_entity import Credentials, Token
from utilities.sanitize import sanitize_json
import json
from utilities.error_handler import ResponseCode
from utilities.logger import LoggerFactory
from requests.exceptions import ConnectionError

'''
authentication.py

This module provides functions for interacting with the authentication server. It is primarily
for obtaining creditionals based on a passed token.

Functions:
    - authentication: recieved a token and returns a credential object or error response.
'''

def authentication(token) -> Credentials:
    '''
    Authenticates users credentials given generated json web token.
    
    Args:
        token: a dictionary in format {'token': <token string>}

    Returns:
        cred: a Credential object initialized from returned credentials.
    '''
    logger=LoggerFactory.get_general_logger()
    secure_logger=LoggerFactory.get_security_logger()

    logger.debug("Begin authenticating token")
    secure_logger.debug("Begin authenticating token.")

    # sanitize token to avoid code injection
    safe_token=sanitize_json(token)
    secure_logger.debug("Token successfully sanitized")
    
    # validate token dict is of proper format
    try:
        logger.debug("Begin validating format of token")
        valid_token_object=Token.from_json_object(safe_token)
        valid_token=valid_token_object.to_json_object()
    except ValueError as e:
        secure_logger.error(e)
        return ResponseCode('InvalidOperation')
    
    # load authenication server uris
    secure_logger.debug("Begin read in config file")
    try:
        data=config_file_reader("./configs/authentication_params.yaml")
        uri=data["uri"]
        ping_uri=data["ping_uri"]
        secure_logger.debug("Successfully loaded config file")
    except:
        secure_logger.error("Unsuccessfully loaded config file")
        return ResponseCode("InvalidName")
    
    # check if server online
    secure_logger.debug("Pinging authentication server.")
    try:
        response=requests.get(ping_uri)
        if response.status_code == 200:
            secure_logger.debug("Authentication Server is up.")
        else:
            raise ConnectionError("Could not connect to server")
    except:
        secure_logger.error("Cannot connect to server")
        return ResponseCode("InvalidOperation")
    
    # send sanitized and valid token to authenication server
    headers={
        "Content-Type": 'application/json'
    }
    try:
        secure_logger.debug("Begin requesting creditionals from authentication server.")
        response=requests.post(uri, json=valid_token, headers=headers)
        json_content=json.loads(response.text)
        secure_logger.debug("Successfully recieved response from authentication server.")
    except:
        # issue reaching server
        secure_logger.error("Issue obtaining credentials from authentication server.")
        return ResponseCode('InvalidOperation')
    
    # sanitize response from authentication server
    secure_logger.debug("Begin sanatize authentication server response")
    safe_content=sanitize_json(json_content)
    secure_logger.debug("Successfully sanitized authentication server.")
    
    # validate credentials follow business rules
    try:
        secure_logger.debug("Begin validating format of recieved credentials.")
        creds=Credentials.from_json_object(safe_content)
        secure_logger.debug("Credentials successfully validated.")
        logger.debug("Successfully loaded credentials.")
        # return credentials object
        return creds
    except ValueError as e:
        secure_logger.error(e)
        return ResponseCode('InvalidOperation') # returns ResponseCode object which logs to general log
        


with open("./configs/jwt.json","r") as json_file:
    token=json.load(json_file)

print(isinstance(authentication(token),ResponseCode))
    

    