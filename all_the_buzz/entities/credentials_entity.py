'''
credentials_entity.py

This module contains entity classes for data related to authentication.

Classes:
    Credentials: An entity class for storing and validating credential information. 
    Token: An entity class for storing and validating the token
'''

class Credentials:
    '''
    Validates credential data passed to it.
    This class includes the id, first name, last name, dept,
    title, and loc information for the user.
    
    To initialize this class, the from_json_object method can be used.
    To do this just pass in a dict in form:
    {'id': <id>, 'fName' : <fName>, 'lName': <lName>,
    'dept': <dept>, 'title':<title>,
    'loc':<loc>}

    All fields are required.
    '''
    def __init__(self, id=0, fName="Mike", lName="Tiger", 
                 dept="Sales", title="Manager", 
                 loc="United States" ):
        self.id=id
        self.fName=fName
        self.lName=lName
        self.dept=dept
        self.title=title
        self.loc=loc

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self,id):
        """
        Validates the ID is the in the proper format and follows
        business logic.
        
        Exceptions:
            ValueError: ID is missing
            ValueError: ID must be integer
            ValueError: ID must not be negative
        """
        if id is None:
            raise ValueError("Missing ID")
        elif not isinstance(id,int):
            raise ValueError("ID must be integer")
        elif id < 0:
            raise ValueError("ID must be not be negative")
        # Add code to handle special characters
        # Add code to test for SQL injection
        else:
            self.__id=id

    @property
    def fName(self):
        return self.__fName
    
    @fName.setter
    def fName(self, fName):
        """
        Validates First Name follows business logic.
        
        Exceptions:
            ValueError: First name must be provide
            ValueError: First name must be string
            ValueError: First name must not be all spaces
            ValueError: First name has too many characters
            """
        if fName is None:
            raise ValueError("First name must be provided")
        elif not isinstance(fName, str):
            raise ValueError("First name must be a string")
        elif len(fName) == 0:
            raise ValueError("First name too short")
        elif len(fName.strip()) == 0:
            raise ValueError("First name can't be all spaces")
        elif len(fName.strip()) > 50:
            raise ValueError('First name is too long ')
        # Add code to handle apostrophes
        # Add code to test for SQL injection
        else:
            self.__fName=fName.strip()
    
    @property
    def lName(self):
        return self.__lName
    
    @lName.setter
    def lName(self,lName):
        """
        Method for validating Last name follows business logic.
        
        Exceptions:
            ValueError: Last name must be provided
            ValueError: Last name must be string
            ValueError: Last name must not be all spaces
            ValueError: Last name has too many characters
            """
        if lName is None:
            raise ValueError("Last name must be provided")
        elif not isinstance(lName, str):
            raise ValueError("Last name must be a string")
        elif len(lName) == 0:
            raise ValueError("Last name too short")
        elif len(lName.strip()) == 0:
            raise ValueError("Last name can't be all spaces")
        elif len(lName.strip()) > 50:
            raise ValueError("Last name too long")
        # Add code to handle apostrophes
        # Add code to test for SQL injection
        else:
            self.__lName=lName.strip()

    @property
    def dept(self):
        return self.__dept
    
    @dept.setter
    def dept(self, dept):
        """
        Method for ensuring dept follows business rules.
        
        Exceptions:
            ValueError: dept must be present
            ValueError: dept must be a string
            ValueError: dept is too long
            ValueError: Deparment must only contain letters
            """
        if dept == None:
            raise ValueError("dept cannot be None")
        elif not isinstance(dept, str):
            raise ValueError("dept must be a string")
        elif len(dept) == 0:
            raise ValueError("dept length cannot be 0")
        elif len(dept.strip()) == 0:
            raise ValueError("dept can't only be spaces")
        elif len(dept) > 35:
            raise ValueError("dept cannot be greater than 35 characters")
        elif not all(part.strip().isalpha() for part in dept.strip().split()):
            raise ValueError("dept must be letters")
        else:
            self.__dept=dept.strip()

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title):
        """
        Method for ensuring title follows business logic.

        Exceptions:
            ValueError: Title must be present
            ValueError: Title must be a string
            ValueError: Title must not be empty
            ValueError: Title is too long
            ValueError: Title must only contain letters
        """
        if title is None:
            raise ValueError("Title cannot be None")
        elif not isinstance(title, str):
            raise ValueError("Title must be a string")
        elif len(title) == 0:
            raise ValueError("Title too short")
        elif len(title.strip()) == 0:
            raise ValueError("Title must not be empty")
        elif len(title.strip()) > 50:
            raise ValueError("Title too long")
        elif not all(part.strip().isalpha() for part in title.strip().split()):
            raise ValueError("Title must be only contain letters")
        else:
            self.__title=title.strip().capitalize()

    @property
    def loc(self):
        return self.__loc
    
    @loc.setter
    def loc(self, loc):
        """
        Method for validating loc follows business logic.
        
        Exceptions:
            ValueError: loc is required
            ValueError: loc must be a string
            ValueError: loc can not be empty
            ValueError: loc has too many characters
            ValueError: loc can only contain letters
            """
        if loc is None:
            raise ValueError("loc cannot be None")
        elif not isinstance(loc, str):
            raise ValueError("loc must be a string")
        elif len(loc) == 0:
            raise ValueError("loc too short")
        elif len(loc.strip()) == 0:
            raise ValueError("loc can not be spaces")
        elif len(loc.strip()) > 75:
            raise ValueError("loc cannot be greater than 75 characters")
        elif not all(part.strip().isalpha() for part in loc.strip().split()):
            raise ValueError("loc can only be letters")
        else:
            self.__loc=loc.strip()

    @staticmethod
    def from_json_object(content):
        """
        Method for initializing Credential object with dictionary. This
        method will also ensure the dictionary has the required fields.
        
        Exception:
            ValueError: Must be a dictionary
            ValueError: Authentication Server Response
            ValueError: Required fields are missing
            """
        requried_fields=['id','fName','lName','dept','title','loc']
        error_field='mesg'
        if not isinstance(content, dict):
            raise ValueError("Must be dictionary input")
        elif error_field in content:
            raise ValueError(content[error_field])
        elif not all(key in content for key in requried_fields):
            raise ValueError("Missing required fields")
        else: 
            if content['title'].capitalize() != 'Manager':
                content['title']='Employee'
        
            return Credentials(content["id"], content["fName"], 
                            content["lName"], content["dept"], 
                            content["title"], content["loc"])
    
    

class Token:
    """
    Entity class for validating the json web tokens.
    """
    def __init__(self, token='ABC'):
        self.token=token

    @property
    def token(self):
        return self.__token
    
    @token.setter
    def token(self,token):
        """
        Method for validating token follows the business logic.

        Exceptions:
            ValueError: Token can not be none
            ValueError: Token must be a string
            ValueError: Token must be not be empty
            ValueError: Token is too short
            ValueError: Token is too long
        """
        if token is None:
            raise ValueError("Token can not be None")
        elif not isinstance(token, str):
            raise ValueError("Token must be string")
        elif len(token) == 0:
            raise ValueError("No token provided")
        elif len(token) < 250:
            raise ValueError("Token is too short")
        elif len(token) > 400:
            raise ValueError("Token is too long")
        else:
            self.__token=token

    @staticmethod
    def from_json_object(content):
        """
        Method for initializing Token object from a dictionary.
        This method also validates the format of the dictionary and ensures
        the token field is present.
        
        Exceptions:
            ValueError: Must be a dictionary
            ValueError: Missing Required fields
            """
        required_fields=['token']
        if not isinstance(content, dict):
            raise ValueError("Must be of type dictionary")
        elif not all(key in content for key in required_fields):
            raise ValueError("Missing Requried fields")
        else:
            return Token(content["token"])
    
    def to_json_object(self):
        return {'token': self.__token}
    
