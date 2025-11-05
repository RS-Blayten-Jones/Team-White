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

# --- PACKAGE PATH FIX FOR DIRECT EXECUTION ---
# This ensures that absolute imports like 'from all_the_buzz.utilities' work
# when the script is run directly (e.g., 'python server.py' or 'python all_the_buzz/server.py').
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from all_the_buzz.utilities.authentication import authentication
from all_the_buzz.entities.credentials_entity import Credentials, Token
from all_the_buzz.entities.record_entities import Joke
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
    (GET /jokes)

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
            status_code, body = ResponseCode(e).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_joke, Joke):
            try:
                dao_response = private_jokes_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode) == True
            except Exception as e:
                private_jokes_dao.clear_credentials()
                status_code, body = ResponseCode(e).to_http_response()
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
            status_code, body = ResponseCode(e).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_joke, Joke):
            try:
                dao_response = public_jokes_dao.create_record(request_body)
                assert isinstance(dao_response, ResponseCode)
            except Exception as e:
                private_jokes_dao.clear_credentials()
                status_code, body = ResponseCode(e).to_http_response()
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
        
@authentication_middleware #this does not work yet
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
            status_code, body = ResponseCode(e).to_http_response()
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
            status_code, body = ResponseCode(e).to_http_response()
            return jsonify(body), status_code
        if isinstance(new_edit, Joke):
            try:
                #calling create record on the private database 
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

@authentication_middleware
def retrieve_private_jokes_collection(credentials: Credentials):
    pass





#do PUT /jokes for employees: calls create on private joke table (creates a new proposal either an edit )
    #for managers 

@authentication_middleware
def approve_joke(credentials: Credentials, id: str):
    if credentials.title == "Manager":
        # set credentials and database
        private_jokes_dao = get_dao_set_credentials(credentials, "PrivateJokeDAO")
        public_jokes_dao = get_dao_set_credentials(credentials, "PublicJokeDAO")
        try:
            record=private_jokes_dao.get_by_key(id)
        except Exception as e:
            status_code, body = ResponseCode(e).to_http_response()
            public_jokes_dao.clear_credentials()
            private_jokes_dao.clear_credentials()
            return jsonify(body), status_code
        
        # Check if valid joke
        try:
            pending_joke=Joke.from_json_object(record)
        except Exception as e:
            status_code, body = ResponseCode(e).to_http_response()
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
                status_code, body = ResponseCode(e).to_http_response()
                public_jokes_dao.clear_credentials()
                private_jokes_dao.clear_credentials()
                return jsonify(body), status_code
        # if pending joke isn't and edit
        elif pending_joke.is_edit == False:
            pending_joke.is_edit=None
            try:
                public_jokes_dao.create_record(pending_joke.to_json_object())
            except Exception as e:
                status_code, body = ResponseCode(e).to_http_response()
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
            status_code, body = ResponseCode(e).to_http_response()
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
            status_code, body = ResponseCode(e).to_http_response()
            private_jokes_dao.clear_credentials()
            return jsonify(body), status_code
    else:
        status_code, body = ResponseCode("Unauthorized").to_http_response()
        return jsonify(body), status_code

@authentication_middleware
def retrieve_random_joke(credentials: Credentials, amt: int):
    if credentials.title == "Manager" or credentials.title == "Employee":
        public_jokes_dao = get_dao_set_credentials(credentials, "PublicJokeDAO")
        try:
            random_jokes=public_jokes_dao.get_random(amt)
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
        all_quotes = public_quotes_dao.get_all_records()
        public_quotes_dao.clear_credentials()
        json_string = dumps(all_quotes)
        ResponseCode("GeneralSuccess", json_string)
        return json_string, 200
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
        public_trivia_dao = get_dao_set_credentials(credentials, "PublicTriviaDAO")
        all_trivia = public_trivia_dao.get_all_records()
        public_trivia_dao.clear_credentials()
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
        "/joke/<string:id>/approve",
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
        "/joke/<string:id>/deny",
        view_func=deny_joke,
        methods=["POST"],
        provide_automatic_options=False
    )
    app.add_url_rule(
        "/random_jokes/<int:amount>",
        view_func=retrieve_random_joke,
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
        "/trivias",
        view_func=retrieve_public_trivia_collection,
        methods=["GET"],
        provide_automatic_options=False
    )
    app.add_url_rule(
        "/bios",
        view_func=retrieve_public_bios_collection,
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