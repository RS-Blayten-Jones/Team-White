from typing import Optional, Any
from all_the_buzz.utilities.logger import LoggerFactory

_RESPONSE_MAP = {
    #PyMongo Errors
    "AutoReconnect": (503, "The operation MAY have succeeded, but the connection to the database was lost. Please retry."),
    "BulkWriteError": (400, "The write operation failed due to invalid data."),
    "CollectionInvalid": (422, "The submitted data does not meet the collection's validation rules"),
    "ConfigurationError": (500, "Database configuration error. Please contact support."),
    "ConnectionFailure": (503, "Unable to connect to the database. Please try again later."),
    "CursorNotFound": (410, "The requested data stream is no longer available."),
    "DocumentTooLarge": (413, "The document is too large to be stored. Please reduce its size or wait for more storage space to be added to the server."),
    "DuplicateKeyError": (409, "A record with this identifier already exists."),
    "EncryptedCollectionError": (422, "Could not create encrypted collection due to invalid configuration."),
    "EncryptionError": (500, "Data encryption failed. Please try again or contact support."),
    "ExecutionTimeout": (504, "The database query took too long and was aborted. Please try again at a later time."),
    "InvalidName": (400, "Invalid collection or database name used in the request."),
    "InvalidOperation": (400, "The requested operation is not allowed in this context."),
    "InvalidURI": (400, "Invalid database connection string. Check your URI format."),
    "NetworkTimeout": (504, "Database operation timed out. The result may be incomplete. Please try again at a later time."),
    "NotPrimaryError": (503, "Database is temporarily unavailable due to server maintenance."),
    "OperationFailure": (500, "The database operation failed. Please check your request and try again."),
    "ProtocolError": (502, "Unexpected response from the database. Please try again."),
    "RefuseToBrew": (418, "Server refused to brew; provide tea instead of coffee or retry with brewer."),
    "ServerSelectionTimeoutError": (503, "Database server is currently unavailable. Please retry shortly."),
    "WTimeoutError": (504, "The write operation did not meet replication requirements in time."),
    "WaitQueueTimeoutError": (503, "Database is busy. Please wait and try again."),
    "WriteConcernError": (500, "The write was successful but did not meet durability requirements."),
    "WriteError": (400, "The write operation failed due to invalid data."),
    "PyMongoError": (500, "An unexpected and unknown database error occurred. Please try again or contact support."),
    "ResourceNotFound": (404, "This resource does not exist in our database."), #Custom error
    
    #Custom Error Calls
        #Token Validation Errors
    "AuthenticationTimeout": (503, "Authentication server did not respond. Try again later."),
    "MalformedAuthenticationResponse": (502, "Authentication server gave a malformed object to the API. Try again later."),
    "UnauthorizedToken": (401, "Token was expired or invalid. Please send a new valid JWT."),
    "MissingToken": (401, "Missing Authentication Token"),
        #API Request Errors
    "MalformedContent": (400, "Request content had malformed syntax. Please check your request."),
    "RateLimit": (429, "Too many requests have been sent. Please wait until you can request again."),
    "Unauthorized": (401, "Unauthorized request"),
    "Internal Authentication Error": (500, "Internal Authentication Error"),
        #Security Errors
    "ChecksumValidationError": (500, "Integrity check failed. Try again later."),
    "FieldValidationError": (400, "One of the fields was of an incorrect type. Please ensure that data is of the correct field type."),
    "LengthValidationError": (413, "One of the fields was too large. Please ensure that data is within acceptable parameters."),
    "PermissionIncongruency": (403, "User does not have the correction permissions required for this action."),

    #Success Codes
    "GeneralSuccess": (200, "OK! Success!"),
    "PostSuccess": (201, "POST succeeded. Here is your database ID."),
    "PendingSuccess": (202, "Your edit or suggested file creation is being processed. It will be denied or approved by a moderator at a later time."),

    #employee title error
    "InvalidEmployee": (400, "Employee title invalid"),
    
    #Authentication Codes
    "InvalidToken": (401, "Authentication failed. Please verify your credentials and try again."),
    "ConfigLoadError": (500, "The configuration could not be loaded. Please verify the file and try again."),
    "ServerConnectionError": (503, "The operation could not be completed due to a lost connection. Please retry."),
    "AuthServerError": (502, "The request could not be completed due to a temporary issue with the authentication service. Please retry."),
    "InvalidEmployee": (400, "Employee title invalid"), #idk if this is actually used 
    #record validation error
    "InvalidRecord": (400, "Record is either invalid or not in valid format"),
    "InvalidFilter": (400, "Filters are either invalid fields or not in valid format")
}

class ResponseCode:
    '''
    This class wraps a detailed HTTP response code with a custom message and added data and automatically
    logs this result 
    '''
    def __init__(self, error_tag: str = "", data: Optional[Any] = None):
        '''
        Args:
            error_tag (str): the name of error that will be passed to the RESPONSE_MAP to get the HTTP error code
            data (any optional): extra data from the operation or error to be sent with the response (defaults to None)
        '''
        self.__logger = LoggerFactory.get_general_logger()
        self.__error_tag = error_tag
        #Defualt to 500 error if it cannot be found in look-up table
        self.__error_code, self.__message = _RESPONSE_MAP.get(error_tag, (500, "An unexpected error occurred."))
        self.__success = (self.__error_code < 300)
        self.__data = data
        if(not self.__success):
            self.__logger.error(f"{self.__error_code}. {error_tag}: {self.__message}\n\t\t\tdata: {self.__data}")
        else:
            self.__logger.info(f"{self.__error_code}. {error_tag}: {self.__message}\n\t\t\tdata: {self.__data}")

    def get_success(self) -> bool:
        return self.__success
    
    def get_error_code(self) -> int:
        return self.__error_code
    
    def get_error_tag(self) -> str:
        return self.__error_tag
    
    def get_message(self) -> str:
        return self.__message
    
    def get_data(self) -> Optional[Any]:
        return self.__data
    
    def to_http_response(self) -> tuple[int, dict]:
        '''
        Creates an HTTP response to send back to the user
        
        Returns:
            response (tuple[int, dict]): a coupled a tuple of the response code and a JSONified version
            of the information stored in ResponseCode
        '''
        response_body = {
            "status": "success" if self.__success else "error",
            "code_tag": self.__error_tag,
            "message": self.__message
        }
        if self.__data is not None:
            response_body["data"] = self.__data
        
        return self.__error_code, response_body