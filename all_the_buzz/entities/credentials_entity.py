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
    This class includes the id, first name, last name, department,
    title, and location information for the user.
    
    To initialize this class, the from_json_object method can be used.
    To do this just pass in a dict in form:
    {'id': <id>, 'fname' : <fname>, 'lname': <lname>,
    'department': <department>, 'title':<title>,
    'location':<location>}

    All fields are required.
    '''
    def __init__(self, id=0, fname="Mike", lname="Tiger", 
                 department="Sales", title="Manager", 
                 location="United States" ):
        self.id=id
        self.fname=fname
        self.lname=lname
        self.department=department
        self.title=title
        self.location=location

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
        else:
            self.__id=id

    @property
    def fname(self):
        return self.__fname
    
    @fname.setter
    def fname(self, fname):
        """
        Validates First Name follows business logic.
        
        Exceptions:
            ValueError: First name must be provide
            ValueError: First name must be string
            ValueError: First name must not be all spaces
            ValueError: First name has too many characters
            """
        if fname is None:
            raise ValueError("First name must be provided")
        elif not isinstance(fname, str):
            raise ValueError("First name must be a string")
        elif len(fname) < 0:
            raise ValueError("First name length cannot be negative")
        elif len(fname.strip()) == 0:
            raise ValueError("First name can't be all spaces")
        elif len(fname.strip()) > 100:
            raise ValueError('First name is too long ')
        else:
            self.__fname=fname.strip()
    
    @property
    def lname(self):
        return self.__lname
    
    @lname.setter
    def lname(self,lname):
        """
        Method for validating Last name follows business logic.
        
        Exceptions:
            ValueError: Last name must be provided
            ValueError: Last name must be string
            ValueError: Last name must not be all spaces
            ValueError: Last name has too many characters
            """
        if lname is None:
            raise ValueError("Last name must be provided")
        elif not isinstance(lname, str):
            raise ValueError("Last name must be a string")
        elif len(lname) < 0:
            raise ValueError("Last name length cannot be negative")
        elif len(lname.strip()) == 0:
            raise ValueError("Last name can't be all spaces")
        elif len(lname.strip()) > 50:
            raise ValueError("Last name must be less than 50 characters")
        else:
            self.__lname=lname.strip()

    @property
    def department(self):
        return self.__department
    
    @department.setter
    def department(self, department):
        """
        Method for ensuring department follows business rules.
        
        Exceptions:
            ValueError: Department must be present
            ValueError: Department must be a string
            ValueError: Department is too long
            ValueError: Deparment must only contain letters
            """
        if department == None:
            raise ValueError("Department cannot be None")
        elif not isinstance(department, str):
            raise ValueError("Department must be a string")
        elif len(department) < 0:
            raise ValueError("Department length cannot be negative")
        elif len(department.strip()) == 0:
            raise ValueError("Department can't only be spaces")
        elif len(department) > 35:
            raise ValueError("Department cannot be greater than 35 characters")
        elif len(department) < 0:
            raise ValueError("Department length cannot be negative")
        elif not all(part.strip().isalpha() for part in department.strip().split()):
            raise ValueError("Department must be letters")
        else:
            self.__department=department.strip()

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
        elif len(title) < 0:
            raise ValueError("Title length cannot be negative")
        elif len(title.strip()) == 0:
            raise ValueError("Title must not be empty")
        elif len(title.strip()) > 100:
            raise ValueError("Title too long")
        elif not all(part.strip().isalpha() for part in title.strip()):
            raise ValueError("Title must be only contain letters")
        else:
            self.__title=title.strip()

    @property
    def location(self):
        return self.__location
    
    @location.setter
    def location(self, location):
        """
        Method for validating location follows business logic.
        
        Exceptions:
            ValueError: Location is required
            ValueError: Location must be a string
            ValueError: Location can not be empty
            ValueError: Location has too many characters
            ValueError: Location can only contain letters
            """
        if location is None:
            raise ValueError("Location cannot be None")
        elif not isinstance(location, str):
            raise ValueError("Location must be a string")
        elif len(location) < 0:
            raise ValueError("Location length cannot be negative")
        elif len(location.strip()) == 0:
            raise ValueError("Location can not be spaces")
        elif len(location.strip()) > 75:
            raise ValueError("Location cannot be greater than 75 characters")
        elif not all(part.isalpha() for part in location.strip().split()):
            raise ValueError("Location can only be letters")
        else:
            self.__location=location.strip()

    @staticmethod
    def from_json_object(content):
        """
        Method for initializing Credential object with dictionary. This
        method will also ensure the dictionary has the required feilds.
        
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
            return Credentials(content["id"], content["fName"], 
                           content["lName"], content["dept"], 
                           content["title"], content["loc"])
    
    

class Token:
    """
    Entity class for the json web tokens.
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
            raise ValueError("Token must be be longer than zero")
        elif len(token) < 250:
            raise ValueError("Token is too short.")
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
    
Token.from_json_object({'token': 'ABC'})
tk=Token('ABC')
tk.token
Credentials()