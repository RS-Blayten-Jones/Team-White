from flask import Flask, request, jsonify, make_response
import utilities.authentication
from typing import Callable, Any
from functools import wraps
from entities.credentials_entity import Credentials, Token
from utilities.error_handler import ResponseCode

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


def run():
    port = 8080
    print(f"Server running on port {port}")
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    run()