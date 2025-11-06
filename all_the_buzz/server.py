from flask import Flask, request, jsonify, make_response
# from all_the_buzz.utilities.authentication import authentication
# from all_the_buzz.utilities.authentication import authentication
from typing import Callable, Any
from functools import wraps
# from all_the_buzz.entities.credentials_entity import Credentials, Token
# from all_the_buzz.entities.record_entities import Joke
# from all_the_buzz.utilities.error_handler import ResponseCode
# from all_the_buzz.database_operations.dao_factory import DAOFactory
# from entities.credentials_entity import Credentials, Token
# from entities.record_entities import Joke
# from utilities.error_handler import ResponseCode
# from database_operations.dao_factory import DAOFactory
from pymongo.errors import PyMongoError
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
#from all_the_buzz.utilities.logger import LoggerFactory
#from utilities.logger import LoggerFactory
from bson.json_util import dumps
from bson.objectid import ObjectId

# --- PACKAGE PATH FIX FOR DIRECT EXECUTION ---
# This ensures that absolute imports like 'from all_the_buzz.utilities' work
# when the script is run directly (e.g., 'python server.py' or 'python all_the_buzz/server.py').
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from all_the_buzz.utilities.authentication import authentication
from all_the_buzz.entities.credentials_entity import Credentials, Token
from all_the_buzz.entities.record_entities import Joke, Trivia, Quote, Bio
from all_the_buzz.utilities.error_handler import ResponseCode
from all_the_buzz.database_operations.dao_factory import DAOFactory
from all_the_buzz.utilities.logger import LoggerFactory
"""

    Get All Jokes
    -------------
    (GET) http://localhost:8080/jokes/

    Included:
        Include Bearer header with token
    Returns:
        Dictonary of all public jokes
    
    Create New Joke
    ---------------
    (POST) http://localhost:8080/jokes
    
    Include:
        Include Bearer header with token
        In body include json object in this format:
        {
            "level": int,
            "language": str,
            "content": {
                "type": <either "one_liner" or "qa">,
                "text": str (required if "one_liner"),
                "question": str (required if "qa"),
                "answer": str (required if "qa")
                }
            }
    Returns:
        Adds joke to public table if manager and adds to private
        table if employee.
     
    Update Joke
    -----------
    (PUT) http://localhost:8080/jokes/<string:joke_id>/
    
    Include:
        Token in Bearer header
        ID of joke in uri
    Returns:
        If present returns a json object of the specifed joke
        in the public table
    
    Approve Joke
    ------------
    (POST) http://localhost:8080/joke/<string:joke-id>/approve/
    
    Include:
        Token in Bearer header
        ID of joke in private table
    Returns:
        If manager updates or adds joke to public table
        Deletes joke from private table 
        
    Deny Joke
    ---------
    (POST) http://localhost:8080/joke/<string:joke-id>/deny/
    
    Include:
        Token in bearer header
        ID of joke in private table
    Returns:
        If manager, deletes joke from private table
        
    Get All Quotes
    --------------
    (GET) http//localhost:8080/quotes/

    Include:
        Token in bearer header
    Returns:
        Returns all quotes from public table
    """
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
SERVER_VER = '1'
def create_client_connection(server_version: str = SERVER_VER) -> ResponseCode:
    try:
        client = DAOFactory.set_client(ATLAS_URI, server_version)
        return ResponseCode("GeneralSuccess", data=client)
    except Exception as e:
        return ResponseCode(e, f"Failed to connect to MongoDB: {str(e)}")


class MyFlask(Flask):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        return super().add_url_rule(rule, endpoint, view_func, **options)

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

def convert_filter_types(filter_dict: dict[str, str]) -> dict[str, Any]:
    """Converts string values in the filter dictionary to their required types (e.g., int)."""
    
    int_fields = ['level', 'birth_year', 'death_year']
    bool_fields = ['is_edit']
    type_safe_filter = {}
    for key, value in filter_dict.items():
        if key in int_fields:
            try:
                type_safe_filter[key] = int(value)
            except ValueError:
                print(f"WARNING: Filter '{key}' received non-integer value '{value}'. Skipping.")
                continue
        elif key in bool_fields:
            lower_value = value.lower()
            if lower_value in ('true'):
                type_safe_filter[key] = True
            elif lower_value in ('false','', ' '):
                type_safe_filter[key] = False
            else:
                print(f"WARNING: Filter '{key}' received non-bool value '{value}'. Skipping.")
                continue
        else:
            type_safe_filter[key] = value
            
    return type_safe_filter

@authentication_middleware
def retrieve_public_jokes_collection(credentials: Credentials):
    """Retrieves the collection of public (approved) jokes.

    This endpoint serves two functions via the GET /jokes route:
    1. **Retrieve All:** Returns ALL public jokes if no query parameters are provided (GET /jokes).
    2. **Filter by Fields:** Returns a filtered list of public jokes if query 
       parameters are provided (e.g., GET /jokes?difficulty=2&category=tech).

    Args:
        credentials: The authenticated user's credentials object, injected by
            the authentication_middleware. This is used to confirm the user is 
            authorized for read access.

    Returns:
        A tuple containing:
        * The JSON string representation of the jokes (filtered or all) and a 200 HTTP status code,
          if the user is authenticated.
        * A tuple containing a JSON error response and a 401 HTTP status code,
          if the user is unauthorized (handled by the credential check).
    """
    if credentials.title == 'Employee' or credentials.title == 'Manager':
        public_jokes_dao = get_dao_set_credentials(credentials, "PublicJokeDAO")
        filter_dict = request.args.to_dict()
        if filter_dict:
            type_safe_filter = convert_filter_types(filter_dict)
            if type_safe_filter:
                all_jokes = public_jokes_dao.get_by_fields(type_safe_filter)
            else:
                all_jokes = []
                public_jokes_dao.clear_credentials()
                status_code, body = ResponseCode("InvalidFilter").to_http_response()
                return jsonify(body), status_code 
        else:
            all_jokes = public_jokes_dao.get_all_records()
        public_jokes_dao.clear_credentials()
        json_string = dumps(all_jokes)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code

@authentication_middleware
def create_a_new_joke(credentials: Credentials):
    
    """
    Handles the creation of a new joke record (POST /jokes).

    The behavior and target collection are strictly determined by the authenticated
    user's title:

    1.  **Manager ('Manager'):** The joke is created directly in the PublicJokeDAO
        collection. This action constitutes immediate approval.
    2.  **Employee ('Employee'):** The joke is created in the PrivateJokeDAO
        collection as a proposal (`is_edit` is set to False), requiring subsequent
        review and approval.

    The request body is first parsed and validated against the Joke entity schema.

    Args:
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware. Used to determine the appropriate DAO
            and access level.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON body, 200/201/202): Success response based on the underlying DAO
            operation (typically 201 for Manager/Public creation, or a status code
            indicating successful proposal submission for Employee/Private).
        * (JSON body, 400): If the JSON request body fails validation via
            `Joke.from_json_object()`.
        * (JSON body, 401/500): If the user title is unrecognized ('InvalidEmployee'),
            or if an exception occurs during the DAO operation (translated via
            ResponseCode error).
    """

    if credentials.title == 'Employee':
        private_jokes_dao = get_dao_set_credentials(credentials, "PrivateJokeDAO")
        request_body = request.get_json()
        request_body["is_edit"] = False
        try:
            new_joke = Joke.from_json_object(request_body)
        except Exception as e:
            private_jokes_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_joke, Joke):
            try:
                dao_response = private_jokes_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode) == True
            except Exception as e:
                private_jokes_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            private_jokes_dao.clear_credentials()
            status_code, body = dao_response.to_http_response()
            return jsonify(body), status_code
        else:
            private_jokes_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
        
    elif credentials.title == 'Manager':
        public_jokes_dao = get_dao_set_credentials(credentials, 'PublicJokeDAO')
        request_body = request.get_json()
        try:
            new_joke = Joke.from_json_object(request_body)
        except Exception as e:
            private_jokes_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_joke, Joke):
            try:
                dao_response = public_jokes_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode)
            except Exception as e:
                private_jokes_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            public_jokes_dao.clear_credentials()
            status_code, body = dao_response.to_http_response()
            return jsonify(body), status_code
        else:
            private_jokes_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
    else:
        private_jokes_dao.clear_credentials()
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code
    




@authentication_middleware
def create_a_new_quote(credentials: Credentials): #employee credentials create in private, manager's create in public
    
    """
    Handles the creation of a new quote record (POST /quote).

    The behavior and target collection are strictly determined by the authenticated
    user's title:

    1.  **Manager ('Manager'):** The joke is created directly in the PublicQuoteDAO
        collection. This action constitutes immediate approval.
    2.  **Employee ('Employee'):** The joke is created in the PrivateQuoteDAO
        collection as a proposal (`is_edit` is set to False), requiring subsequent
        review and approval.

    The request body is first parsed and validated against the Quote entity schema.

    Args:
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware. Used to determine the appropriate DAO
            and access level.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON body, 200/201/202): Success response based on the underlying DAO
            operation (typically 201 for Manager/Public creation, or a status code
            indicating successful proposal submission for Employee/Private).
        * (JSON body, 400): If the JSON request body fails validation via
            `Quote.from_json_object()`.
        * (JSON body, 401/500): If the user title is unrecognized ('InvalidEmployee'),
            or if an exception occurs during the DAO operation (translated via
            ResponseCode error).
    """

    if credentials.title == 'Employee':
        private_quotes_dao = get_dao_set_credentials(credentials, "PrivateQuoteDAO")
        request_body = request.get_json()
        request_body["is_edit"] = False
        try:
            new_quote = Quote.from_json_object(request_body)
        except Exception as e:
            private_quotes_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_quote, Quote):
            try:
                dao_response = private_quotes_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode) == True
            except Exception as e:
                private_quotes_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            private_quotes_dao.clear_credentials()
            status_code, body = dao_response.to_http_response()
            return jsonify(body), status_code
        else:
            private_quotes_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
        
    elif credentials.title == 'Manager':
        public_quotes_dao = get_dao_set_credentials(credentials, 'PublicQuoteDAO')
        request_body = request.get_json()
        try:
            new_joke = Quote.from_json_object(request_body)
        except Exception as e:
            private_quotes_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_quote, Quote):
            try:
                dao_response = public_quotes_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode)
            except Exception as e:
                private_quotes_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            public_quotes_dao.clear_credentials()
            status_code, body = dao_response.to_http_response()
            return jsonify(body), status_code
        else:
            private_quotes_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
    else:
        private_quotes_dao.clear_credentials()
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code
    

    


@authentication_middleware
def create_a_new_trivia(credentials: Credentials): #employee credentials create in private, manager's create in public
    
    """
    Handles the creation of a new trivia record (POST /trivias).

    The behavior and target collection are strictly determined by the authenticated
    user's title:

    1.  **Manager ('Manager'):** The trivia is created directly in the PublicTriviaDAO
        collection. This action constitutes immediate approval.
    2.  **Employee ('Employee'):** The trivia is created in the PublicTriviaDAO
        collection as a proposal (`is_edit` is set to False), requiring subsequent
        review and approval.

    The request body is first parsed and validated against the trivia entity schema.

    Args:
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware. Used to determine the appropriate DAO
            and access level.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON body, 200/201/202): Success response based on the underlying DAO
            operation (typically 201 for Manager/Public creation, or a status code
            indicating successful proposal submission for Employee/Private).
        * (JSON body, 400): If the JSON request body fails validation via
            `trivia.from_json_object()`.
        * (JSON body, 401/500): If the user title is unrecognized ('InvalidEmployee'),
            or if an exception occurs during the DAO operation (translated via
            ResponseCode error).
    """

    if credentials.title == 'Employee':
        private_trivias_dao = get_dao_set_credentials(credentials, "PrivateTriviaDAO")
        request_body = request.get_json()
        request_body["is_edit"] = False
        try:
            new_trivia = Trivia.from_json_object(request_body)
        except Exception as e:
            private_trivias_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_trivia, Trivia):
            try:
                dao_response = private_trivias_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode) == True
            except Exception as e:
                private_trivias_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            private_trivias_dao.clear_credentials()
            status_code, body = dao_response.to_http_response()
            return jsonify(body), status_code
        else:
            private_trivias_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
        
    elif credentials.title == 'Manager':
        public_trivias_dao = get_dao_set_credentials(credentials, 'PublicTriviaDAO')
        request_body = request.get_json()
        try:
            new_trivia = Trivia.from_json_object(request_body)
        except Exception as e:
            private_trivias_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_trivia, Trivia):
            try:
                dao_response = public_trivias_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode)
            except Exception as e:
                private_trivias_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            public_trivias_dao.clear_credentials()
            status_code, body = dao_response.to_http_response()
            return jsonify(body), status_code
        else:
            private_trivias_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
    else:
        private_trivias_dao.clear_credentials()
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code




@authentication_middleware
def create_a_new_bio(credentials: Credentials): #employee credentials create in private, manager's create in public
    
    """
    Handles the creation of a new bio record (POST /bio).

    The behavior and target collection are strictly determined by the authenticated
    user's title:

    1.  **Manager ('Manager'):** The bio is created directly in the PublicBioDAO
        collection. This action constitutes immediate approval.
    2.  **Employee ('Employee'):** The bio is created in the PublicBioDAO
        collection as a proposal (`is_edit` is set to False), requiring subsequent
        review and approval.

    The request body is first parsed and validated against the bio entity schema.

    Args:
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware. Used to determine the appropriate DAO
            and access level.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON body, 200/201/202): Success response based on the underlying DAO
            operation (typically 201 for Manager/Public creation, or a status code
            indicating successful proposal submission for Employee/Private).
        * (JSON body, 400): If the JSON request body fails validation bio.from_json_object()`.
        * (JSON body, 401/500): If the user title is unrecognized ('InvalidEmployee'),
            or if an exception occurs during the DAO operation (translated via
            ResponseCode error).
    """

    if credentials.title == 'Employee':
        private_bios_dao = get_dao_set_credentials(credentials, "PrivateBioDAO")
        request_body = request.get_json()
        request_body["is_edit"] = False
        try:
            new_bio = Bio.from_json_object(request_body)
        except Exception as e:
            private_bios_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_bio, Bio):
            try:
                dao_response = private_bios_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode) == True
            except Exception as e:
                private_bios_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            private_bios_dao.clear_credentials()
            status_code, body = dao_response.to_http_response()
            return jsonify(body), status_code
        else:
            private_bios_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
        
    elif credentials.title == 'Manager':
        public_bios_dao = get_dao_set_credentials(credentials, 'PublicBioDAO')
        request_body = request.get_json()
        try:
            new_bios = Trivia.from_json_object(request_body)
        except Exception as e:
            private_bios_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_bios, Trivia):
            try:
                dao_response = public_trivias_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode)
            except Exception as e:
                private_bios_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            public_bios_dao.clear_credentials()
            status_code, body = dao_response.to_http_response()
            return jsonify(body), status_code
        else:
            private_bios_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
    else:
        private_bios_dao.clear_credentials()
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code



        
@authentication_middleware
def update_joke(joke_id: str, credentials: Credentials):
    """
    (PUT /jokes/<joke_id>) for updating or proposing an edit.
    
    The function validates the incoming JSON request body against the Joke entity 
    schema for all users. The target action is strictly determined by the authenticated
    user's title:

    1.  **Manager ('Manager'):** Executes a direct `update_record` on the specified 
        public joke ID within the PublicJokeDAO collection.
    2.  **Employee ('Employee'):** Executes a `create_record` (submission) in the 
        PrivateJokeDAO collection. The request body is tagged with the original 
        `joke_id` (as 'original_id') and flagged as an edit (`is_edit=True`).

    Args:
        joke_id: The unique identifier (ID) of the public joke targeted for update.
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware, used to determine write authority.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON body, 200): Successful **direct update** by a Manager.
        * (JSON body, 202): Successful submission of a **pending edit proposal** by an Employee.
        * (JSON body, 400): If the request body fails entity validation 
        (`Joke.from_json_object`) or is an otherwise invalid record.
        * (JSON body, 401/500): If the user is unauthorized or if a database 
        exception occurs during the DAO operation (translated via ResponseCode).
    """
    request_body = request.get_json()
    if credentials.title == 'Manager':
        public_jokes_dao = get_dao_set_credentials(credentials, "PublicJokeDAO")
        #entity validation
        try:
            updated_joke = Joke.from_json_object(request_body)
        except Exception as e:
            #entity validation fails
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        #actual database update
        if isinstance(updated_joke, Joke):
            try:
                print(joke_id)
                get_response = public_jokes_dao.get_by_fields({'_id': str(joke_id)})
                print(get_response)
                dao_response = public_jokes_dao.update_record(str(joke_id), request_body)
                public_jokes_dao.clear_credentials()
                status_code, body = dao_response.to_http_response()
                return jsonify(body), status_code
            except Exception as e:
                public_jokes_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
        else:
            public_jokes_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
    elif credentials.title == 'Employee':
        private_jokes_dao = DAOFactory.get_dao('PrivateJokeDAO')
        private_jokes_dao.set_credentials(credentials)
        #setting the OG id of the record to edit and setting is edit to true
        request_body["original_id"] = joke_id
        request_body["is_edit"] = True
        try:
            new_edit = Joke.from_json_object(request_body)
        except Exception as e:
            private_jokes_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_edit, Joke):
            try:
                #calling create record on the private database 
                request_body["original_id"] = ObjectId(joke_id)
                dao_response = private_jokes_dao.create_record(request_body)
                private_jokes_dao.clear_credentials()
                status_code, body = ResponseCode("PendingSuccess").to_http_response()
                return jsonify(body), status_code 
            except Exception as e:
                private_jokes_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code
    


@authentication_middleware #this does not work yet
def update_trivia(trivia_id: str, credentials: Credentials):
    """
    (PUT /trivia/<trivia_id>) for updating or proposing an edit.
    
    The function validates the incoming JSON request body against the Trivia entity 
    schema for all users. The target action is strictly determined by the authenticated
    user's title:

    1.  **Manager ('Manager'):** Executes a direct `update_record` on the specified 
        public trivia ID within the PublicTriviaDAO collection.
    2.  **Employee ('Employee'):** Executes a `create_record` (submission) in the 
        PrivateTriviaDAO collection. The request body is tagged with the original 
        `trivia_id` (as 'original_id') and flagged as an edit (`is_edit=True`).

    Args:
        trivia_id: The unique identifier (ID) of the public trivia targeted for update.
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware, used to determine write authority.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON body, 200): Successful **direct update** by a Manager.
        * (JSON body, 202): Successful submission of a **pending edit proposal** by an Employee.
        * (JSON body, 400): If the request body fails entity validation 
        (`Trivia.from_json_object`) or is an otherwise invalid record.
        * (JSON body, 401/500): If the user is unauthorized or if a database 
        exception occurs during the DAO operation (translated via ResponseCode).
    """
    request_body = request.get_json()
    if credentials.title == 'Manager':
        public_trivias_dao = get_dao_set_credentials(credentials, "PublicTriviaDAO")
        #entity validation
        try:
            updated_trivia = Trivia.from_json_object(request_body)
        except Exception as e:
            #entity validation fails
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        #actual database update
        if isinstance(updated_trivia, Trivia):
            try:
                print(trivia_id)
                get_response = public_trivias_dao.get_by_fields({'_id': str(trivia_id)})
                print(get_response)
                dao_response = public_trivias_dao.update_record(str(trivia_id), request_body)
                public_trivias_dao.clear_credentials()
                status_code, body = dao_response.to_http_response()
                return jsonify(body), status_code
            except Exception as e:
                public_trivias_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
        else:
            public_trivias_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
    elif credentials.title == 'Employee':
        private_trivias_dao = DAOFactory.get_dao('PrivateTriviaDAO')
        private_trivias_dao.set_credentials(credentials)
        #setting the OG id of the record to edit and setting is edit to true
        request_body["original_id"] = trivia_id
        request_body["is_edit"] = True
        try:
            new_edit = Trivia.from_json_object(request_body)
        except Exception as e:
            private_trivias_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_edit, Trivia):
            try:
                #calling create record on the private database 
                print(new_edit)
                request_body["original_id"] = ObjectId(trivia_id)
                dao_response = private_trivias_dao.create_record(request_body)
                print(dao_response.get_data())
                private_trivias_dao.clear_credentials()
                status_code, body = ResponseCode("PendingSuccess").to_http_response()
                return jsonify(body), status_code 
            except Exception as e:
                private_trivias_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code


@authentication_middleware #this does not work yet
def update_quote(quote_id: str, credentials: Credentials):
    """
    (PUT /quote/<quote_id>) for updating or proposing an edit.
    
    The function validates the incoming JSON request body against the quote entity 
    schema for all users. The target action is strictly determined by the authenticated
    user's title:

    1.  **Manager ('Manager'):** Executes a direct `update_record` on the specified 
        public quote ID within the PublicQuoteDAO collection.
    2.  **Employee ('Employee'):** Executes a `create_record` (submission) in the 
        PrivateQuoteDAO collection. The request body is tagged with the original 
        `quote_id` (as 'original_id') and flagged as an edit (`is_edit=True`).

    Args:
        quote_id: The unique identifier (ID) of the public quote targeted for update.
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware, used to determine write authority.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON body, 200): Successful **direct update** by a Manager.
        * (JSON body, 202): Successful submission of a **pending edit proposal** by an Employee.
        * (JSON body, 400): If the request body fails entity validation 
        (`quote.from_json_object`) or is an otherwise invalid record.
        * (JSON body, 401/500): If the user is unauthorized or if a database 
        exception occurs during the DAO operation (translated via ResponseCode).
    """
    request_body = request.get_json()
    if credentials.title == 'Manager':
        public_quotes_dao = get_dao_set_credentials(credentials, "PublicQuoteDAO")
        #entity validation
        try:
            updated_quote = Quote.from_json_object(request_body)
        except Exception as e:
            #entity validation fails
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        #actual database update
        if isinstance(updated_quote, Quote):
            try:
                print(quote_id)
                get_response = public_quotes_dao.get_by_fields({'_id': str(quote_id)})
                print(get_response)
                dao_response = public_quotes_dao.update_record(str(quote_id), request_body)
                public_quotes_dao.clear_credentials()
                status_code, body = dao_response.to_http_response()
                return jsonify(body), status_code
            except Exception as e:
                public_quotes_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
        else:
            public_quotes_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
    elif credentials.title == 'Employee':
        private_quotes_dao = DAOFactory.get_dao('PrivateQuoteDAO')
        private_quotes_dao.set_credentials(credentials)
        #setting the OG id of the record to edit and setting is edit to true
        request_body["original_id"] = quote_id
        request_body["is_edit"] = True
        try:
            new_edit = Quote.from_json_object(request_body)
        except Exception as e:
            private_quotes_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_edit, Quote):
            try:
                #calling create record on the private database 
                print(new_edit)
                request_body["original_id"] = ObjectId(quote_id)
                dao_response = private_quotes_dao.create_record(request_body)
                print(dao_response.get_data())
                private_quotes_dao.clear_credentials()
                status_code, body = ResponseCode("PendingSuccess").to_http_response()
                return jsonify(body), status_code 
            except Exception as e:
                private_quotes_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            

@authentication_middleware #this does not work yet
def update_bio(bio_id: str, credentials: Credentials):
    """
    (PUT /bio/<bio_id>) for updating or proposing an edit.
    
    The function validates the incoming JSON request body against the bio entity 
    schema for all users. The target action is strictly determined by the authenticated
    user's title:

    1.  **Manager ('Manager'):** Executes a direct `update_record` on the specified 
        public bio ID within the PublicBioDAO collection.
    2.  **Employee ('Employee'):** Executes a `create_record` (submission) in the 
        PrivateBioDAO collection. The request body is tagged with the original 
        `bio_id` (as 'original_id') and flagged as an edit (`is_edit=True`).

    Args:
        bio_id: The unique identifier (ID) of the public bio targeted for update.
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware, used to determine write authority.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON body, 200): Successful **direct update** by a Manager.
        * (JSON body, 202): Successful submission of a **pending edit proposal** by an Employee.
        * (JSON body, 400): If the request body fails entity validation 
        (`bio.from_json_object`) or is an otherwise invalid record.
        * (JSON body, 401/500): If the user is unauthorized or if a database 
        exception occurs during the DAO operation (translated via ResponseCode).
    """
    request_body = request.get_json()
    if credentials.title == 'Manager':
        public_bios_dao = get_dao_set_credentials(credentials, "B")
        #entity validation
        try:
            updated_bio = Bio.from_json_object(request_body)
        except Exception as e:
            #entity validation fails
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        #actual database update
        if isinstance(updated_bio, Bio):
            try:
                print(bio_id)
                get_response = public_bios_dao.get_by_fields({'_id': str(bio_id)})
                print(get_response)
                dao_response = public_bios_dao.update_record(str(bio_id), request_body)
                public_bios_dao.clear_credentials()
                status_code, body = dao_response.to_http_response()
                return jsonify(body), status_code
            except Exception as e:
                public_bios_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
        else:
            public_bios_dao.clear_credentials()
            status_code, body = ResponseCode("InvalidRecord").to_http_response()
            return jsonify(body), status_code
    elif credentials.title == 'Employee':
        private_bios_dao = DAOFactory.get_dao('PrivateBioDAO')
        private_bios_dao.set_credentials(credentials)
        #setting the OG id of the record to edit and setting is edit to true
        request_body["original_id"] = bio_id
        request_body["is_edit"] = True
        try:
            new_edit = Bio.from_json_object(request_body)
        except Exception as e:
            private_bios_dao.clear_credentials()
            status_code, body = ResponseCode(str(e)).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_edit, Bio):
            try:
                #calling create record on the private database 
                print(new_edit)
                request_body["original_id"] = ObjectId(bio_id)
                dao_response = private_bios_dao.create_record(request_body)
                print(dao_response.get_data())
                private_bios_dao.clear_credentials()
                status_code, body = ResponseCode("PendingSuccess").to_http_response()
                return jsonify(body), status_code 
            except Exception as e:
                private_bios_dao.clear_credentials()
                status_code, body = ResponseCode(str(e)).to_http_response()
                return jsonify(body), status_code
            


            
            

@authentication_middleware
def retrieve_private_jokes_collection(credentials: Credentials):
    """
    Retrieves the collection of private (pending) joke proposals (GET /pending_jokes).

    This endpoint provides access to the private database collection, which stores
    all proposed jokes and edits submitted by Employees that are pending review
    by a Manager. Access is strictly controlled.

    Args:
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware, used to verify the user's title.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON string, 200): If the user is a **Manager**, returns a JSON string
        containing all records from the PrivateJokeDAO collection.
        * (JSON body, 401): If the user is **not a Manager** (e.g., an Employee or
        any other role), returns an "Unauthorized" error response.
    """

    if credentials.title == 'Manager':
        private_jokes_dao = get_dao_set_credentials(credentials, "PrivateJokeDAO")
        all_private_jokes = private_jokes_dao.get_all_records()
        private_jokes_dao.clear_credentials()
        json_string = dumps(all_private_jokes)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code


@authentication_middleware
def retrieve_private_quotes_collection(credentials: Credentials):
    """
    Retrieves the collection of private (pending) quote proposals (GET /pending_quotes).

    This endpoint provides access to the private database collection, which stores
    all proposed quotes and edits submitted by Employees that are pending review
    by a Manager. Access is strictly controlled.

    Args:
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware, used to verify the user's title.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON string, 200): If the user is a **Manager**, returns a JSON string
        containing all records from the PrivatequoteDAO collection.
        * (JSON body, 401): If the user is **not a Manager** (e.g., an Employee or
        any other role), returns an "Unauthorized" error response.
    """

    if credentials.title == 'Manager':
        private_quotes_dao = get_dao_set_credentials(credentials, "PrivateQuoteDAO")
        all_private_quotes = private_quotes_dao.get_all_records()
        private_quotes_dao.clear_credentials()
        json_string = dumps(all_private_quotes)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code
    


@authentication_middleware
def retrieve_private_bios_collection(credentials: Credentials):
    """
    Retrieves the collection of private (pending) bio proposals (GET /pending_bios).

    This endpoint provides access to the private database collection, which stores
    all proposed bios and edits submitted by Employees that are pending review
    by a Manager. Access is strictly controlled.

    Args:
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware, used to verify the user's title.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON string, 200): If the user is a **Manager**, returns a JSON string
        containing all records from the PrivatebioDAO collection.
        * (JSON body, 401): If the user is **not a Manager** (e.g., an Employee or
        any other role), returns an "Unauthorized" error response.
    """

    if credentials.title == 'Manager':
        private_bios_dao = get_dao_set_credentials(credentials, "PrivateBioDAO")
        all_private_bios = private_bios_dao.get_all_records()
        private_bios_dao.clear_credentials()
        json_string = dumps(all_private_bios)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code
    


@authentication_middleware
def retrieve_private_trivias_collection(credentials: Credentials):
    """
    Retrieves the collection of private (pending) trivia proposals (GET /pending_trivias).

    This endpoint provides access to the private database collection, which stores
    all proposed trivias and edits submitted by Employees that are pending review
    by a Manager. Access is strictly controlled.

    Args:
        credentials: The authenticated user's Credentials object, injected by
            the authentication_middleware, used to verify the user's title.

    Returns:
        A tuple containing a JSON response body and an HTTP status code:
        * (JSON string, 200): If the user is a **Manager**, returns a JSON string
        containing all records from the PrivateTriviaDAO collection.
        * (JSON body, 401): If the user is **not a Manager** (e.g., an Employee or
        any other role), returns an "Unauthorized" error response.
    """

    if credentials.title == 'Manager':
        private_trivias_dao = get_dao_set_credentials(credentials, "PrivateTriviaDAO")
        all_private_trivias = private_trivias_dao.get_all_records()
        private_trivias_dao.clear_credentials()
        json_string = dumps(all_private_trivias)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code
    


@authentication_middleware
def approve_joke(credentials: Credentials, id: str):
    if credentials.title == "Manager":
        # set credentials and database
        private_jokes_dao = get_dao_set_credentials(credentials, "PrivateJokeDAO")
        public_jokes_dao = get_dao_set_credentials(credentials, "PublicJokeDAO")
        try:
            record=private_jokes_dao.get_by_key(id)
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_jokes_dao.clear_credentials()
            private_jokes_dao.clear_credentials()
            return jsonify(body), status_code
        
        # check if valid joke
        try:
            pending_joke=Joke.from_json_object(record)
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_jokes_dao.clear_credentials()
            private_jokes_dao.clear_credentials()
            return jsonify(body), status_code
        # if pending joke is an edit
        if pending_joke.is_edit == True:
            original_id=pending_joke.ref_id
            pending_joke.is_edit=None
            pending_joke.ref_id=None
            try:
                public_jokes_dao.update_record(original_id,pending_joke.to_json_object())
            except Exception as e:
                status_code, body = ResponseCode(str(e)).to_http_response()
                public_jokes_dao.clear_credentials()
                private_jokes_dao.clear_credentials()
                return jsonify(body), status_code
        # if pending joke isn't and edit
        elif pending_joke.is_edit == False:
            pending_joke.is_edit=None
            try:
                public_jokes_dao.create_record(pending_joke.to_json_object())
            except Exception as e:
                status_code, body = ResponseCode(str(e)).to_http_response()
                public_jokes_dao.clear_credentials()
                private_jokes_dao.clear_credentials()
                return jsonify(body), status_code
        try:
            dao_response=private_jokes_dao.delete_record(id)
            status_code, body = dao_response.to_http_response()
            public_jokes_dao.clear_credentials()
            private_jokes_dao.clear_credentials()
            return jsonify(body), status_code
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_jokes_dao.clear_credentials()
            private_jokes_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        public_jokes_dao.clear_credentials()
        private_jokes_dao.clear_credentials()
        return jsonify(body), status_code

@authentication_middleware
def deny_joke(credentials: Credentials, id: str):
    if credentials.title == "Manager":
        private_jokes_dao = get_dao_set_credentials(credentials, "PrivateJokeDAO")
        try:
            dao_response=private_jokes_dao.delete_record(id)
            status_code, body = dao_response.to_http_response()
            private_jokes_dao.clear_credentials()
            return jsonify(body), status_code
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            private_jokes_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code
    

@authentication_middleware
def approve_quote(credentials: Credentials, id: str):
    if credentials.title == "Manager":
        # set credentials and database
        private_quotes_dao = get_dao_set_credentials(credentials, "PrivateQuoteDAO")
        public_quotes_dao = get_dao_set_credentials(credentials, "PublicQuoteDAO")
        try:
            record=private_quotes_dao.get_by_key(id)
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_quotes_dao.clear_credentials()
            private_quotes_dao.clear_credentials()
            return jsonify(body), status_code
        
        # Check if valid quote
        try:
            pending_quote=Quote.from_json_object(record)
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_quotes_dao.clear_credentials()
            private_quotes_dao.clear_credentials()
            return jsonify(body), status_code
        # if pending quote is an edit
        if pending_quote.is_edit == True:
            original_id=pending_quote.ref_id
            pending_quote.is_edit=None
            pending_quote.ref_id=None
            try:
                public_quotes_dao.update_record(original_id,pending_quote.to_json_object())
            except Exception as e:
                status_code, body = ResponseCode(str(e)).to_http_response()
                public_quotes_dao.clear_credentials()
                private_quotes_dao.clear_credentials()
                return jsonify(body), status_code
        # if pending quote isn't and edit
        elif pending_quote.is_edit == False:
            pending_quote.is_edit=None
            try:
                public_quotes_dao.create_record(pending_quote.to_json_object())
            except Exception as e:
                status_code, body = ResponseCode(str(e)).to_http_response()
                public_quotes_dao.clear_credentials()
                private_quotes_dao.clear_credentials()
                return jsonify(body), status_code
        try:
            dao_response=private_quotes_dao.delete_record(id)
            status_code, body = dao_response.to_http_response()
            public_quotes_dao.clear_credentials()
            private_quotes_dao.clear_credentials()
            return jsonify(body), status_code
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_quotes_dao.clear_credentials()
            private_quotes_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        public_quotes_dao.clear_credentials()
        private_quotes_dao.clear_credentials()
        return jsonify(body), status_code

@authentication_middleware
def deny_quote(credentials: Credentials, id: str):
    if credentials.title == "Manager":
        private_quotes_dao = get_dao_set_credentials(credentials, "PrivateQuoteDAO")
        try:
            dao_response=private_quotes_dao.delete_record(id)
            status_code, body = dao_response.to_http_response()
            private_quotes_dao.clear_credentials()
            return jsonify(body), status_code
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            private_quotes_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code



@authentication_middleware
def approve_trivia(credentials: Credentials, id: str):
    if credentials.title == "Manager":
        # set credentials and database
        private_trivias_dao = get_dao_set_credentials(credentials, "PrivateTriviaDAO")
        public_trivias_dao = get_dao_set_credentials(credentials, "PublicTriviaDAO")
        try:
            record=private_trivias_dao.get_by_key(id)
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_trivias_dao.clear_credentials()
            private_trivias_dao.clear_credentials()
            return jsonify(body), status_code
        
        # Check if valid trivia
        try:
            pending_trivia=Trivia.from_json_object(record)
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_trivias_dao.clear_credentials()
            private_trivias_dao.clear_credentials()
            return jsonify(body), status_code
        # if pending trivia is an edit
        if pending_trivia.is_edit == True:
            original_id=pending_trivia.ref_id
            pending_trivia.is_edit=None
            pending_trivia.ref_id=None
            try:
                public_trivias_dao.update_record(original_id,pending_trivia.to_json_object())
            except Exception as e:
                status_code, body = ResponseCode(str(e)).to_http_response()
                public_trivias_dao.clear_credentials()
                private_trivias_dao.clear_credentials()
                return jsonify(body), status_code
        # if pending trivia isn't and edit
        elif pending_trivia.is_edit == False:
            pending_trivia.is_edit=None
            try:
                public_trivias_dao.create_record(pending_trivia.to_json_object())
            except Exception as e:
                status_code, body = ResponseCode(str(e)).to_http_response()
                public_trivias_dao.clear_credentials()
                private_trivias_dao.clear_credentials()
                return jsonify(body), status_code
        try:
            dao_response=private_trivias_dao.delete_record(id)
            status_code, body = dao_response.to_http_response()
            public_trivias_dao.clear_credentials()
            private_trivias_dao.clear_credentials()
            return jsonify(body), status_code
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_trivias_dao.clear_credentials()
            private_trivias_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        public_trivias_dao.clear_credentials()
        private_trivias_dao.clear_credentials()
        return jsonify(body), status_code

@authentication_middleware
def deny_trivia(credentials: Credentials, id: str):
    if credentials.title == "Manager":
        private_trivias_dao = get_dao_set_credentials(credentials, "PrivateTriviaDAO")
        try:
            dao_response=private_trivias_dao.delete_record(id)
            status_code, body = dao_response.to_http_response()
            private_trivias_dao.clear_credentials()
            return jsonify(body), status_code
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            private_trivias_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code
    

@authentication_middleware
def approve_bio(credentials: Credentials, id: str):
    if credentials.title == "Manager":
        # set credentials and database
        private_bios_dao = get_dao_set_credentials(credentials, "PrivateBioDAO")
        public_bios_dao = get_dao_set_credentials(credentials, "PublicBioDAO")
        try:
            record=private_bios_dao.get_by_key(id)
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_bios_dao.clear_credentials()
            private_bios_dao.clear_credentials()
            return jsonify(body), status_code
        
        # Check if valid bio
        try:
            pending_bio=Bio.from_json_object(record)
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_bios_dao.clear_credentials()
            private_bios_dao.clear_credentials()
            return jsonify(body), status_code
        # if pending bio is an edit
        if pending_bio.is_edit == True:
            original_id=pending_bio.ref_id
            pending_bio.is_edit=None
            pending_bio.ref_id=None
            try:
                public_bios_dao.update_record(original_id,pending_bio.to_json_object())
            except Exception as e:
                status_code, body = ResponseCode(str(e)).to_http_response()
                public_bios_dao.clear_credentials()
                private_bios_dao.clear_credentials()
                return jsonify(body), status_code
        # if pending bio isn't and edit
        elif pending_bio.is_edit == False:
            pending_bio.is_edit=None
            try:
                public_bios_dao.create_record(pending_bio.to_json_object())
            except Exception as e:
                status_code, body = ResponseCode(str(e)).to_http_response()
                public_bios_dao.clear_credentials()
                private_bios_dao.clear_credentials()
                return jsonify(body), status_code
        try:
            dao_response=private_bios_dao.delete_record(id)
            status_code, body = dao_response.to_http_response()
            public_bios_dao.clear_credentials()
            private_bios_dao.clear_credentials()
            return jsonify(body), status_code
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_bios_dao.clear_credentials()
            private_bios_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        public_bios_dao.clear_credentials()
        private_bios_dao.clear_credentials()
        return jsonify(body), status_code

@authentication_middleware
def deny_bio(credentials: Credentials, id: str):
    if credentials.title == "Manager":
        private_bios_dao = get_dao_set_credentials(credentials, "PrivateBioDAO")
        try:
            dao_response=private_bios_dao.delete_record(id)
            status_code, body = dao_response.to_http_response()
            private_bios_dao.clear_credentials()
            return jsonify(body), status_code
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            private_bios_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code


@authentication_middleware
def retrieve_random_joke(credentials: Credentials, amount: int):
    if credentials.title == "Manager" or credentials.title == "Employee":
        public_jokes_dao = get_dao_set_credentials(credentials, "PublicJokeDAO")
        try:
            random_jokes=public_jokes_dao.get_random(amount)
            json_string = dumps(random_jokes)
            ResponseCode("GeneralSuccess", json_string)
            public_jokes_dao.clear_credentials()
            return json_string, 200
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_jokes_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code

@authentication_middleware
def retrieve_short_quote(credentials: Credentials, amount: int):
    if credentials.title == "Manager" or credentials.title == "Employee":
        public_quote_dao = get_dao_set_credentials(credentials, "PublicQuoteDAO")
        try:
            short_quotes=public_quote_dao.get_short_record(amount)
            json_string = dumps(short_quotes)
            ResponseCode("GeneralSuccess", json_string)
            public_quotes_dao.clear_credentials()
            return json_string, 200
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_jokes_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code
#quotes
@authentication_middleware
def retrieve_public_quotes_collection(credentials: Credentials):
    """
    Retrieves the public quote collection and returns it as a http response
    (GET /quotes)


    This endpoint is accessible to any authenticated user (employee or manager)
    and returns all records stored in the PublicQuotesDAO collection. It handles
    serialization of MongoDB records (including BSON types like ObjectId) to a 
    valid JSON string.

    Args:
        credentials: The authenticated user's credentials object, injected by
        the authentication_middleware.

    Returns:
        A tuple containing:
        * The JSON string representation of all public quotes and a 200 HTTP status code, if the user is authenticated.
        * A tuple containing a JSON error response and a 401 HTTP status code, if the user is unauthorized 
    """
    if credentials.title == 'Employee' or credentials.title == 'Manager':
        public_quotes_dao = get_dao_set_credentials(credentials, "PublicQuoteDAO")

        filter_dict = request.args.to_dict()
        if filter_dict:
            type_safe_filter = convert_filter_types(filter_dict)
            if type_safe_filter:
                all_quotes = public_quotes_dao.get_by_fields(type_safe_filter)
            else:
                all_quotes = []
                public_quotes_dao.clear_credentials()
                status_code, body = ResponseCode("InvalidFilter").to_http_response()
                return jsonify(body), status_code 
        else:
            all_quotes = public_quotes_dao.get_all_records()

        public_quotes_dao.clear_credentials()
        json_string = dumps(all_quotes)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code

@authentication_middleware
def retrieve_daily_quote(credentials: Credentials):
    if credentials.title == "Manager" or credentials.title == "Employee":
        public_quotes_dao=get_dao_set_credentials(credentials, "PublicQuoteDAO")
        try:
            random_quote=public_quotes_dao.get_quote_of_day()
            print(f"HERE IS THE TYPE: {type(random_quote.get_data())}")
            json_string=dumps(random_quote.get_data())
            ResponseCode("GeneralSuccess", json_string)
            public_bios_dao.clear_credentials()
            return json_string, 200
        except Exception as e:
            status_code, body = ResponseCode(str(e)).to_http_response()
            public_quotes_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code

#trivia
@authentication_middleware
def retrieve_public_trivia_collection(credentials: Credentials):
    """
    Retrieves the public trivia collection and returns it as a http response
    (GET /trivias)

    This endpoint is accessible to any authenticated user (employee or manager)
    and returns all records stored in the PublicTriviaDAO collection. It handles
    serialization of MongoDB records (including BSON types like ObjectId) to a 
    valid JSON string.

    Args:
        credentials: The authenticated user's credentials object, injected by
        the authentication_middleware.

    Returns:
        A tuple containing:
        * The JSON string representation of all public quotes and a 200 HTTP status code, if the user is authenticated.
        * A tuple containing a JSON error response and a 401 HTTP status code, if the user is unauthorized 
    """
    if credentials.title == 'Employee' or credentials.title == 'Manager':
        public_trivias_dao = get_dao_set_credentials(credentials, "PublicTriviaDAO")
        
        filter_dict = request.args.to_dict()
        if filter_dict:
            type_safe_filter = convert_filter_types(filter_dict)
            if type_safe_filter:
                all_trivia = public_trivias_dao.get_by_fields(type_safe_filter)
            else:
                all_trivia = []
                public_trivias_dao.clear_credentials()
                status_code, body = ResponseCode("InvalidFilter").to_http_response()
                return jsonify(body), status_code 
        else:
            all_trivia = public_trivias_dao.get_all_records()

        public_trivias_dao.clear_credentials()
        json_string = dumps(all_trivia)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code


#bios
@authentication_middleware
def retrieve_public_bios_collection(credentials: Credentials):
    """
    Retrieves the public bios collection and returns it as a http response
    (GET /bios)

    This endpoint is accessible to any authenticated user (employee or manager)
    and returns all records stored in the PublicBiosDAO collection. It handles
    serialization of MongoDB records (including BSON types like ObjectId) to a 
    valid JSON string.

    Args:
        credentials: The authenticated user's credentials object, injected by
        the authentication_middleware.

    Returns:
        A tuple containing:
        * The JSON string representation of all public quotes and a 200 HTTP status code, if the user is authenticated.
        * A tuple containing a JSON error response and a 401 HTTP status code, if the user is unauthorized 
    """
    if credentials.title == 'Employee' or credentials.title == 'Manager':
        public_bios_dao = get_dao_set_credentials(credentials, "PublicBioDAO")
        
        filter_dict = request.args.to_dict()
        if filter_dict:
            type_safe_filter = convert_filter_types(filter_dict)
            if type_safe_filter:
                all_bios = public_bios_dao.get_by_fields(type_safe_filter)
            else:
                all_bios = []
                public_bios_dao.clear_credentials()
                status_code, body = ResponseCode("InvalidFilter").to_http_response()
                return jsonify(body), status_code 
        else:
            all_bios = public_bios_dao.get_all_records()
        
        public_bios_dao.clear_credentials()
        json_string = dumps(all_bios)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code


def establish_all_daos():

    global public_jokes_dao
    global private_jokes_dao

    global public_quotes_dao
    global private_quotes_dao

    global public_trivias_dao
    global private_trivias_dao

    global public_bios_dao
    global private_bios_dao
    try:
        public_jokes_dao = DAOFactory.create_dao("PublicJokeDAO", DATABASE_NAME)
        private_jokes_dao = DAOFactory.create_dao("PrivateJokeDAO", DATABASE_NAME)

        public_quotes_dao = DAOFactory.create_dao("PublicQuoteDAO", DATABASE_NAME)
        private_quotes_dao = DAOFactory.create_dao("PrivateQuoteDAO", DATABASE_NAME)

        public_bios_dao = DAOFactory.create_dao("PublicBioDAO", DATABASE_NAME)
        private_bios_dao = DAOFactory.create_dao("PrivateBioDAO", DATABASE_NAME)

        public_trivias_dao = DAOFactory.create_dao("PublicTriviaDAO", DATABASE_NAME)
        private_trivias_dao = DAOFactory.create_dao("PrivateTriviaDAO", DATABASE_NAME)
        print("created")
    except Exception as RuntimeError:
        raise ResponseCode("Issue Creating DAOs", RuntimeError)
    
        

def create_app():
    """Application factory: initializes Flask app and external resources."""
    app = MyFlask(__name__)
    try:
        create_client_connection()
        establish_all_daos()
    except Exception as e:
        print(f"CRITICAL SHUTDOWN: Failed to initialize application resources: {e}")
        raise
    
    app.add_url_rule(
        "/jokes", 
        view_func=retrieve_public_jokes_collection, 
        methods=["GET"],
        provide_automatic_options=False
    )
    """
    Create New Joke
    ---------------
    (POST) http://localhost:8080/jokes
    
    Include:
        Include Bearer header with token
        In body include json object in this format:
        {
            "level": int,
            "language": str,
            "content": {
                "type": <either "one_liner" or "qa">,
                "text": str (required if "one_liner"),
                "question": str (required if "qa"),
                "answer": str (required if "qa")
                }
            }
    Returns:
        Adds joke to public table if manager and adds to private
        table if employee.
        """
    app.add_url_rule(
        "/pending-jokes",
        view_func=retrieve_private_jokes_collection,
        methods=["GET"],
        provide_automatic_options=False
    )
    app.add_url_rule(
        "/jokes", 
        view_func=create_a_new_joke, 
        methods=["POST"],
        provide_automatic_options=False
    )

    """"
    Update Joke
    -----------
    (PUT) http://localhost:8080/jokes/<string:joke_id>/
    
    Include:
        Token in Bearer header
        ID of joke in uri
    Returns:
        If present returns a json object of the specifed joke
        in the public table
    """
    app.add_url_rule(
        "/jokes/<string:joke_id>", 
        view_func=update_joke, 
        methods=["PUT"],
        provide_automatic_options=False
    )
    """
    Approve Joke
    ------------
    (POST) http://localhost:8080/joke/<string:joke-id>/approve/
    
    Include:
        Token in Bearer header
        ID of joke in private table
    Returns:
        If manager updates or adds joke to public table
        Deletes joke from private table 
        """
    app.add_url_rule(
        "/jokes/<string:id>/approve",
        view_func=approve_joke,
        methods=["POST"],
        provide_automatic_options=False
    )
    """
    Deny Joke
    ---------
    (POST) http://localhost:8080/joke/<string:joke-id>/deny/
    
    Include:
        Token in bearer header
        ID of joke in private table
    Returns:
        If manager, deletes joke from private table
        """
    app.add_url_rule(
        "/jokes/<string:id>/deny",
        view_func=deny_joke,
        methods=["POST"],
        provide_automatic_options=False
    )
    app.add_url_rule(
        "/random-jokes/<int:amount>",
        view_func=retrieve_random_joke,
        methods=['GET'],
        provide_automatic_options=False
    )
    app.add_url_rule(
        "/short-quotes/<int:amount>",
        view_func=retrieve_short_quote,
        methods=['GET'],
        provide_automatic_options=False
    )
    """
    Get All Quotes
    --------------
    (GET) http//localhost:8080/quotes/

    Include:
        Token in bearer header
    Returns:
        Returns all quotes from public table
    """
    app.add_url_rule(
        "/quotes",
        view_func=retrieve_public_quotes_collection,
        methods=["GET"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/quotes", 
        view_func=create_a_new_quote, 
        methods=["POST"],
        provide_automatic_options=False

    )

    app.add_url_rule(
        "/quotes/<string:quote_id>", 
        view_func=update_quote, 
        methods=["PUT"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/quotes/<string:id>/approve",
        view_func=approve_quote,
        methods=["POST"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/quotes/<string:id>/deny",
        view_func=deny_quote,
        methods=["POST"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/pending-quotes",
        view_func=retrieve_private_quotes_collection,
        methods=["GET"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/daily_quotes",
        view_func=retrieve_daily_quote,
        methods=["GET"],
        provide_automatic_options=False        
    )
    app.add_url_rule(
        "/trivias",
        view_func=retrieve_public_trivia_collection,
        methods=["GET"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/trivias", 
        view_func=create_a_new_trivia, 
        methods=["POST"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/trivias/<string:trivia_id>", 
        view_func=update_trivia, 
        methods=["PUT"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/trivias/<string:id>/approve",
        view_func=approve_trivia,
        methods=["POST"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/trivias/<string:id>/deny",
        view_func=deny_trivia,
        methods=["POST"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/pending-trivias",
        view_func=retrieve_private_trivias_collection,
        methods=["GET"],
        provide_automatic_options=False
    )
 
    app.add_url_rule(
        "/bios",
        view_func=retrieve_public_bios_collection,
        methods=["GET"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/bios", 
        view_func=create_a_new_bio, 
        methods=["POST"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/bios/<string:bio_id>", 
        view_func=update_bio, 
        methods=["PUT"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/bios/<string:id>/approve",
        view_func=approve_bio,
        methods=["POST"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/bios/<string:id>/deny",
        view_func=deny_bio,
        methods=["POST"],
        provide_automatic_options=False
    )

    app.add_url_rule(
        "/pending-bios",
        view_func=retrieve_private_bios_collection,
        methods=["GET"],
        provide_automatic_options=False
    )


    return app

def run(): 
    port = 8080
    print(f"Server running on port {port}")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    app = create_app()
    run()