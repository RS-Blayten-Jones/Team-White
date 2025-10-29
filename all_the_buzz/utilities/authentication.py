import requests
from utilities.config import config_file_reader
from entities.credentials_entity import Credentials, Token
from utilities.sanitize import sanitize_json
import json

'''
This module contains a function authenticating a token. It requires an input of token which 
is a dictionary in form {'token': <token string> }.
'''

def authentication(token):
    
    # sanitize token
    safe_token=sanitize_json(token)

    # validate token 
    try:
        valid_token_object=Token.from_json_object(safe_token)
        valid_token=valid_token_object.to_json_object()
    except ValueError as e:
        pass
    
    # load authenication server url
    data=config_file_reader("./config_files/authentication_params.yaml")
    url=data["url"]
    
    # send sanitized and valid token to authenication server
    headers={
        "Content-Type": 'application/json'
    }
    try:
        response=requests.post(url, json=valid_token, headers=headers)
        json_content=json.loads(response.text)
    except:
        return "issue reaching authenitication server"
    # sanitize response from authentication server
    safe_content=sanitize_json(json_content)
    
    # validate credentials follow business rules
    try:
        creds=Credentials.from_json_object(safe_content)
        return creds
    except ValueError as e:
        print(e)
        #log here 
        


with open("./config_files/jwt.json","r") as json_file:
    token=json.load(json_file)

print(authentication(token))
    

    