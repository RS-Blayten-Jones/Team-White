'''
credentials_entity.py

This module contains entity classes for data related to the authentication.

Classes:
    Credentials: An entity class for storing and validating credential information. 
    Token: An entity class for storing and validating the token
'''

# house all entity classes
class Credentials:
    '''
    Validates credential data passed to it.
    This class includes the id, first name, last name, department,
    title, and location information for the user.
    
    To initialize this class, you can use the from_json_object method.
    To do this just pass in a dict in form:
    {'id': <id>, 'fname' : <fname>, 'lname': <lname>,
    'department': <department>, 'title':<title>,
    'location':<location>}

    All fields are required.
    '''
    def __init__(self, id="0", fname="Mike", lname="Tiger", 
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
        if id is None:
            raise ValueError("Missing ID")
        elif not isinstance(id, str):
            raise ValueError("Id must be string")
        elif len(id) == 0:
            raise ValueError("ID too short")

        else:
            self.__id=id

    @property
    def fname(self):
        return self.__fname
    
    @fname.setter
    def fname(self, fname):
        # check business logic
        if fname is None:
            raise ValueError("First name must be provided")
        elif not isinstance(fname, str):
            raise ValueError("First name must be a string")
        elif len(fname) == 0:
            raise ValueError("First name too short")
        elif len(fname.strip()) == 0:
            raise ValueError("First name can't be all spaces")
        elif len(fname.strip()) > 50:
            raise ValueError("First name must be less than 50 characters")
        elif not all(part.isalpha() for part in fname.strip().split()):
            raise ValueError("First name must be letters")
        else:
            self.__fname=fname.strip()
    
    @property
    def lname(self):
        return self.__lname
    
    @lname.setter
    def lname(self,lname):
        if lname is None:
            raise ValueError("Last name must be provided")
        elif not isinstance(lname, str):
            raise ValueError("Last name must be a string")
        elif len(lname) == 0:
            raise ValueError("Last name too short")
        elif len(lname.strip()) == 0:
            raise ValueError("Last name can't be all spaces")
        elif len(lname.strip()) > 50:
            raise ValueError("Last name must be less than 50 characters")
        elif not all(part.isalpha() for part in lname.strip().split()):
            raise ValueError("Last name must be letters")
        else:
            self.__lname=lname.strip()

    @property
    def department(self):
        return self.__department
    
    @department.setter
    def department(self, department):
        if department == None:
            raise ValueError("Department cannot be None")
        elif not isinstance(department, str):
            raise ValueError("Department must be a string")
        elif len(department) == 0:
            raise ValueError("Department length cannot be 0")
        elif len(department.strip()) == 0:
            raise ValueError("Department can't only be spaces")
        elif len(department) > 35:
            raise ValueError("Department cannot be greater than 35 characters")
        elif not all(part.isalpha() for part in department.strip().split()):
            raise ValueError("Department must be letters")
        else:
            self.__department=department.strip()

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title):
        print("hi")
        if title is None:
            raise ValueError("Title cannot be None")
        elif not isinstance(title, str):
            raise ValueError("Title must be a string")
        elif len(title) == 0:
            raise ValueError("Title too short")
        elif len(title.strip()) == 0:
            raise ValueError("Title can't only be spaces")
        elif len(title.strip()) > 50:
            raise ValueError("Title cannot be greater than 50 characters")
        elif not all(part.isalpha() for part in title.strip().split()):
            raise ValueError("Title must be only contain letters")
        else:
            self.__title=title.strip()

    @property
    def location(self):
        return self.__location
    
    @location.setter
    def location(self, location):
        if location is None:
            raise ValueError("Location cannot be None")
        elif not isinstance(location, str):
            raise ValueError("Location must be a string")
        elif len(location) == 0:
            raise ValueError("Location too short")
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
        #check is content has proper fields (maybe validation schema)
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
    def __init__(self, token=None):
        self.__token = token

    @property
    def token(self):
        return self.__token
    
    @token.setter
    def token(self,token):
        if token is None:
            raise ValueError("Token can not be None")
        elif not isinstance(token, str):
            raise ValueError("Token must be a string")
        elif len(token) < 250:
            raise ValueError("Token is too short")
        elif len(token) > 400:
            raise ValueError("Token is too long")
        else:
            self.__token=token

    @staticmethod
    def from_json_object(content):
        #check content is proper type
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