from flask import Flask, request, jsonify, make_response
from utilities.authentication import authentication
from typing import Callable, Any
from functools import wraps
from entities.credentials_entity import Credentials, Token
from utilities.error_handler import ResponseCode
from database_operations.dao_factory import DAOFactory
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


global mongo_client

global public_jokes_dao
global private_jokes_dao

global public_quotes_dao
global private_quotes_dao

global public_trivia_dao
global private_trivia_dao

global public_bio_dao
global private_bio_dao


ATLAS_URI = os.getenv("ATLAS_URI") 
DATABASE_NAME = "team_white_database"
def create_mongodb_connection():
    load_dotenv() 
    if not ATLAS_URI:
        raise ValueError("ATLAS_URI environment variable not set. Check your .env file.")
    try:
        client = MongoClient(ATLAS_URI, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("MongoDB client initialized successfully.")
        return client

    except Exception as PyMongoError:
        print(f"ERROR: Failed to connect to MongoDB: {PyMongoError}")
        raise ResponseCode(str(PyMongoError))


class MyFlask(Flask):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        return super().add_url_rule(rule, endpoint, view_func, provide_automatic_options=False, **options)

app = MyFlask(__name__)
#CORS Preflight necessary only when we integrate with front end 

#middleware 
def authentication_middleware(f: Callable) -> Callable:
    """
    Function decorator that extracts the token from a request,
    authenticates it with the function in authentication.py,
    and injects a Credentials object or returns a ResponseCode 
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        user_token = Token(request.headers.get('Bearer'))
        authentication_result = authentication(user_token)
        #if the authentication result is an error code
        if isinstance(authentication_result, ResponseCode):
            status_code, body = authentication_result.to_http_response()
            return jsonify(body), status_code
        #if the authentication result is valid credentials
        if isinstance(authentication_result, Credentials):
            kwargs['credentials'] = authentication_result
            return f(*args, **kwargs)
        #returns 500 error if authentication result is something other than a ResponseCode object or a Credentials object
        status_code, body = ResponseCode("Internal Authentication Error").to_http_response()
        return jsonify(body), status_code
    return decorated_function


@ app.route("/jokes", methods=["GET"])
@authentication_middleware
def retrieve_public_jokes_collection(credentials: Credentials):
    if credentials.title:
        #grab the jokes public dao object
        #all_jokes = jokes_public_dao.get_all_jokes()
        #return jsonify(all_jokes), 200
        pass
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code


def establish_all_daos(client):
    try:
        public_jokes_dao = DAOFactory.create_dao("PublicJokeDAO", mongo_client, DATABASE_NAME)
        private_jokes_dao = DAOFactory.create_dao("PrivateJokeDAO", mongo_client, DATABASE_NAME)

        public_quotes_dao = DAOFactory.create_dao("PublicQuoteDAO", mongo_client, DATABASE_NAME)
        private_quotes_dao = DAOFactory.create_dao("PrivateQuoteDAO", mongo_client, DATABASE_NAME)

        public_bios_dao = DAOFactory.create_dao("PublicBioDAO", mongo_client, DATABASE_NAME)
        private_bios_dao = DAOFactory.create_dao("PrivateBioDAO", mongo_client, DATABASE_NAME)

        public_trivias_dao = DAOFactory.create_dao("PublicTriviaDAO", mongo_client, DATABASE_NAME)
        private_trivias_dao = DAOFactory.create_dao("PrivateTriviaDAO", mongo_client, DATABASE_NAME)
    except Exception as RuntimeError:
        raise ResponseCode("Issue Creating DAOs", RuntimeError)
        


def run(): 
    mongo_client = create_mongodb_connection()
    establish_all_daos()
    port = 8080
    print(f"Server running on port {port}")
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    run()