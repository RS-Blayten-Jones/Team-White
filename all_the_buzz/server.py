from flask import Flask, request
import authentication
from entities.credentials_entity import Credentials
from utilities.error_handler import ResponseCode

class MyFlask(Flask):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        return super().add_url_rule(rule, endpoint, view_func, provide_automatic_options=False, **options)

app = MyFlask(__name__)
#CORS Preflight necessary only when we integrate with front end 

@ app.route("/jokes", methods=["GET"])
def retrieve_public_jokes_collection():
    #get the token from the header 
    user_token = request.headers.get('Bearer')
    if user_token: #if the token is not null
        try:
            cred_or_response_code = authentication(user_token) #creates a Credentials object if valid or response code object 
            if isinstance(cred_or_response_code, ResponseCode): #if it is a response code, just return it
                return cred_or_response_code
            if isinstance(cred_or_response_code, Credentials):
                #if credentials.role == manager, post new joke to public jokes table
                #else, post new joke to private jokes table
                pass

        except Exception as e: #error at authentication function in authentication.py
            return ResponseCode(error_tag=e, data=e)


        

    pass
