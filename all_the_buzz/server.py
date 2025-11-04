from flask import Flask, request, jsonify, make_response
from utilities.authentication import authentication
from typing import Callable, Any
from functools import wraps
from entities.credentials_entity import Credentials, Token
from entities.record_entities import Joke
from utilities.error_handler import ResponseCode
from database_operations.dao_factory import DAOFactory
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pathlib import Path
from utilities.logger import LoggerFactory
from bson.json_util import dumps


global mongo_client

global public_jokes_dao
global private_jokes_dao

global public_quotes_dao
global private_quotes_dao

global public_trivias_dao
global private_trivias_dao

global public_bios_dao
global private_bios_dao

BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / '.env'

load_dotenv(dotenv_path) 
    

ATLAS_URI = os.getenv("ATLAS_URI") 
DATABASE_NAME = "team_white_database"
def create_mongodb_connection():
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


# class MyFlask(Flask):
#     def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
#         return super().add_url_rule(rule, endpoint, view_func, provide_automatic_options=False, **options)
class MyFlask(Flask):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        return super().add_url_rule(rule, endpoint, view_func, **options)

#app = MyFlask(__name__)
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
        try:
            #get user token from request
            user_token = request.headers.get('Bearer')
        except:
            #send back a credentials missing response
            missing_token_result = ResponseCode("MissingToken")
            status_code, body = missing_token_result.to_http_response()
            return jsonify(body), status_code
        token_dict = {'token': str(user_token)}
        try:
            print("trying authentication")
            authentication_result = authentication(token_dict)
        except Exception as e:
            print("authentication error")
        #if the authentication result is an error code
        if isinstance(authentication_result, ResponseCode):
            status_code, body = authentication_result.to_http_response()
            return jsonify(body), status_code
        #if the authentication result is valid credentials
        if isinstance(authentication_result, Credentials):
            kwargs['credentials'] = authentication_result
            return f(*args, **kwargs)
        #returns 500 error if authentication result is something other than a ResponseCode object or a Credentials object
        
        print(f"Authentication results: {authentication_result}")
        print(f"Authentication result type: {type(authentication_result)}")
        status_code, body = ResponseCode("Internal Authentication Error").to_http_response()
        return jsonify(body), status_code
    return decorated_function

def get_dao_set_credentials(credentials: Credentials, dao_classname: str):
    """
    A helper function that returns a dao object after
    setting it's credentials 

    Args:
        credentials: The authenticated user's credentials object, injected by
        the authentication_middleware.
    Returns:
        A (DatabaseAccessObject): a DatabaseAccessObject of the given dao_class_name string
    """
    dao = DAOFactory.get_dao(dao_classname)
    dao.set_credentials(credentials)
    return dao


@authentication_middleware
def retrieve_public_jokes_collection(credentials: Credentials):
    """
    Retrieves the public joke collection and returns it as a http response

    This endpoint is accessible to any authenticated user (employee or manager)
    and returns all records stored in the PublicJokeDAO collection. It handles
    serialization of MongoDB records (including BSON types like ObjectId) to a 
    valid JSON string.

    Args:
        credentials: The authenticated user's credentials object, injected by
        the authentication_middleware.

    Returns:
        A tuple containing:
        * The JSON string representation of all public jokes and a 200 HTTP status code, if the user is authenticated.
        * A tuple containing a JSON error response and a 401 HTTP status code, if the user is unauthorized 
    """
    if credentials.title == 'Employee' or credentials.title == 'Manager':
        public_jokes_dao = get_dao_set_credentials(credentials, "PublicJokeDAO")
        all_jokes = public_jokes_dao.get_all_records()
        public_jokes_dao.clear_credentials()
        json_string = dumps(all_jokes)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code

@authentication_middleware
def create_a_new_joke(credentials: Credentials): #employee credentials create in private, manager's create in public
    #need to find out first if the credentials are for a manager or not 
    # joke_object = request.get_json()
    # print(joke_object)
    # return "Ok", 200
    if credentials.title == 'Employee':
        private_jokes_dao = DAOFactory.get_dao("PrivateJokeDAO")
        private_jokes_dao.set_credentials(credentials)
        request_body = request.get_json()
        request_body["is_edit"] = False
        try:
            new_joke = Joke.from_json_object(request_body)
            print(new_joke)
        except Exception as e:
            status_code, body = ResponseCode(e).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_joke, Joke):
            try:
                print(request_body)
                json_joke = new_joke.to_json_
                dao_response = private_jokes_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode) == True
            except Exception as e:
                status_code, body = ResponseCode(e).to_http_response()
                return jsonify(body), status_code
            private_jokes_dao.clear_credentials()
            status_code, body = dao_response.to_http_response()
            return jsonify(body), status_code
        else:
            return "Error", 400
#do PUT /jokes for employees: calls create on private joke table (creates a new proposal either an edit )
    #for managers 

def establish_all_daos(client):

    global public_jokes_dao
    global private_jokes_dao

    global public_quotes_dao
    global private_quotes_dao

    global public_trivias_dao
    global private_trivias_dao

    global public_bios_dao
    global private_bios_dao
    try:
        public_jokes_dao = DAOFactory.create_dao("PublicJokeDAO", client, DATABASE_NAME)
        private_jokes_dao = DAOFactory.create_dao("PrivateJokeDAO", client, DATABASE_NAME)

        public_quotes_dao = DAOFactory.create_dao("PublicQuoteDAO", client, DATABASE_NAME)
        private_quotes_dao = DAOFactory.create_dao("PrivateQuoteDAO", client, DATABASE_NAME)

        public_bios_dao = DAOFactory.create_dao("PublicBioDAO", client, DATABASE_NAME)
        private_bios_dao = DAOFactory.create_dao("PrivateBioDAO", client, DATABASE_NAME)

        public_trivias_dao = DAOFactory.create_dao("PublicTriviaDAO", client, DATABASE_NAME)
        private_trivias_dao = DAOFactory.create_dao("PrivateTriviaDAO", client, DATABASE_NAME)
        print("created")
    except Exception as RuntimeError:
        raise ResponseCode("Issue Creating DAOs", RuntimeError)
    
        


# def run(): 
#     #establish_all_daos(mongo_client)
#     port = 8080
#     print(f"Server running on port {port}")
#     app.run(host='0.0.0.0', port=port)
    # global mongo_client
    # mongo_client = create_mongodb_connection()
    # establish_all_daos(mongo_client)

# if __name__ == '__main__':
#     run()

# def create_app():
#     app = MyFlask(__name__)

#     # Code to run before the first request (during app initialization)
#     with app.app_context():
#         # Example: Initialize database, load configuration, etc.
#         print("Initializing application resources...")
#         # init_db() 
#         # load_config()
#         global mongo_client
#         mongo_client = create_mongodb_connection()
#         establish_all_daos(mongo_client)

#     return app
def create_app():
    """Application factory: initializes Flask app and external resources."""
    app = MyFlask(__name__)
    try:
        mongo_client = create_mongodb_connection()
        establish_all_daos(mongo_client)
    except Exception as e:
        print(f"CRITICAL SHUTDOWN: Failed to initialize application resources: {e}")
        raise

    app.add_url_rule(
        "/jokes", 
        view_func=retrieve_public_jokes_collection, 
        methods=["GET"],
        provide_automatic_options=False
    )
    app.add_url_rule(
        "/jokes", 
        view_func=create_a_new_joke, 
        methods=["POST"],
        provide_automatic_options=False
    )
    # Add other routes (e.g., /proposals, /quotes) here using the same pattern

    return app

def run(): 
    port = 8080
    print(f"Server running on port {port}")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    app = create_app()
    run()