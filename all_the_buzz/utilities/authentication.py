import requests
from all_the_buzz.utilities.config import config_file_reader
from all_the_buzz.entities.credentials_entity import Credentials, Token
from all_the_buzz.utilities.sanitize import sanitize_json
import json
from all_the_buzz.utilities.error_handler import ResponseCode
from all_the_buzz.utilities.logger import LoggerFactory
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

    # sanitize token to avoid code injection
    safe_token=sanitize_json(token)
    logger.debug("Token successfully sanitized")
    
    # validate token dict is of proper format
    try:
        logger.debug("Begin validating format of token")
        valid_token_object=Token.from_json_object(safe_token)
        valid_token=valid_token_object.to_json_object()
        logger.debug("Token validated")
        #print(f" token in line 45 of authentication.py {valid_token}")
    except ValueError as e:
        logger.error(e)
        return ResponseCode('InvalidToken')
    
    # load authenication server uris
    logger.debug("Begin read in config file")
    try:
        data=config_file_reader("./configs/authentication_params.yaml")
        uri=data["uri"]
        ping_uri=data["ping_uri"]
        logger.debug("Successfully loaded config file")
    except:
        return ResponseCode("ConfigLoadError")
    
    # check if server online
    logger.debug("Pinging authentication server.")
    try:
        response=requests.get(ping_uri)
        if response.status_code == 200:
            logger.debug("Authentication Server is up.")
        else:
            raise ConnectionError("Could not connect to server")
    except:
        return ResponseCode("ServerConnectionError")
    
    # send sanitized and valid token to authenication server
    headers={
        "Content-Type": 'application/json'
    }
    try:
        logger.debug("Begin requesting credentionals from authentication server.")
        response=requests.post(uri, json=valid_token, headers=headers)
        json_content=json.loads(response.text)
        logger.debug("Successfully recieved response from authentication server.")
    except:
        # issue reaching server
        logger.error("Issue obtaining credentials from authentication server.")
        return ResponseCode('AuthServerError')
    
    # sanitize response from authentication server
    logger.debug("Begin sanatize authentication server response")
    safe_content=sanitize_json(json_content)
    logger.debug("Successfully sanitized authentication server.")
    
    # validate credentials follow business rules
    try:
        logger.debug("Begin validating format of recieved credentials.")
        #print(safe_content)
        creds=Credentials.from_json_object(safe_content)
        #print(f"credentials object line 97 of authentication.py {creds}")
        logger.debug("Credentials successfully validated.")
        logger.debug("Successfully loaded credentials.")
        # return credentials object
        secure_logger.info(f"{creds.fname} {creds.lname} credentials successfully validated")
        return creds
    except ValueError as e:
        #print(e)
        logger.error(e)
        return ResponseCode('UnauthorizedToken') # returns ResponseCode object which logs to general log
        
    

    