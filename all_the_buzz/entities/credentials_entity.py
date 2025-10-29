# house all entity classes
class Credentials:
    def __init__(self, id=0, fname="Mike", lname="Tiger", 
                 role="Manager", department="Sales", 
                 title="Manager", location="United States" ):
        self.__id=id
        self.__fname=fname
        self.__lname=lname
        self.__role=role
        self.__department=department
        self.__title=title
        self.__location=location

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self,id):
        if id is None:
            raise ValueError("Missing ID")
        elif not isinstance(id,int):
            raise ValueError("Id must be integer")
        elif id < 0:
            raise ValueError("ID must be zero or higher")
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
        elif not isinstance(fname,str):
            raise ValueError("First name must be string")
        elif len(fname.strip()) == 0:
            raise ValueError("First name can't be all spaces")
        elif len(fname.strip()) > 100:
            raise ValueError('First name is ')
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
        elif not isinstance(lname,str):
            raise ValueError("Last name must be string")
        elif len(lname.strip()) < 0:
            raise ValueError("Last name can't be all spaces")
        elif len(lname.strip()) > 100:
            raise ValueError("Last name is too long")
        elif not all(part.isalpha() for part in lname.strip().split()):
            raise ValueError("Last name must be letters")
        else:
            self.__fname=lname.strip()

    @property
    def role(self):
        return self.__role
    
    @role.setter
    def role(self, role):
        if role is None:
            raise ValueError("Role must be present")
        elif not isinstance(role, str):
            raise ValueError("Role must be a string")
        elif len(role.strip()) == 0:
            raise ValueError("Role must not be all spaces")
        elif len(role.strip()) > 50:
            raise ValueError("Role is too long")
        elif not all(part.isalpha() for part in role.strip().split()):
            raise ValueError("Role must only be alphabet")
        else:
            self.__role=role

    @property
    def department(self):
        return self.__department
    
    @department.setter
    def department(self, department):
        if department == None:
            raise ValueError("Department must be present")
        elif not isinstance(department, str):
            raise ValueError("Department must be string")
        elif len(department) > 100:
            raise ValueError("Department is too long")
        elif not all(part.isalpha() for part in department.strip().split()):
            raise ValueError("Department must be letters")
        else:
            self.__department=department.strip()

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title):
        if title is None:
            raise ValueError("Title is nessacary")
        elif not isinstance(title, str):
            raise ValueError("Title must be string")
        elif len(title.strip()) == 0:
            raise ValueError("Title must be")
        elif len(title.strip()) > 100:
            raise ValueError("Title too long")
        elif not all(part.isalpha() for part in title.strip().split().strip()):
            raise ValueError("Title must be only contain letters")
        else:
            self.__title=title.strip()

    @property
    def location(self):
        return self.__location
    
    @location.setter
    def location(self, location):
        if location is None:
            raise ValueError("Location is required")
        elif not isinstance(location,str):
            raise ValueError("Location must be string")
        elif len(location.strip()) == 0:
            raise ValueError("Location can not be empty")
        elif len(location.strip()) > 100:
            raise ValueError("Location too long")
        elif not all(part.isalpha() for part in location.strip().split().strip()):
            raise ValueError("Location can only be letters")
        else:
            self.__location=location.strip()

    @staticmethod
    def from_json_object(content):
        #check is content has proper fields (maybe validation schema)
        return Credentials(content["id"], content["first_name"], 
                           content["last_name"], content["role"],
                           content["department"], content["title"],
                           content["location"])
    
    def to_json_object(self):
        pass

person=Credentials()
print(person.title)

class Token:
    def __init__(self, token):
        self.__token=token

    @property
    def token(self):
        return self.__token
    @token.setter
    def token(self,token):
        if token is None:
            raise ValueError("Token can not be empty")
        elif not isinstance(token, str):
            raise ValueError("Token must be string")
        elif len(token) == 0:
            raise ValueError("Token must be be longer than zero")
        elif len(token) >200:
            raise ValueError("Token is too long")
        else:
            self.__token=token

    @staticmethod
    def from_json_object(content):
        return Token(content["token"])
    
    def to_json_object(self):
        return {'token': self.__token}