# house all entity classes
from abc import ABC, abstractmethod

class BaseRecord(ABC):
    def __init__(self, id=None, ref_id=None, is_edit=False,
                  content="Haha", language="english"):
        self.id=id
        self.ref_id=ref_id
        self.is_edit=is_edit
        self.content=content
        self.language=language

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id):
        return self.__id 
    
    @property
    def ref_id(self):
        return self.__ref_id
    
    @ref_id.setter 
    def ref_id(self,ref_id):
        return self.__ref_id
    
    @property
    def is_edit(self):
        return self.__is_edit
    
    @is_edit.setter
    def is_edit(self, is_edit):
        return self.__is_edit
    
    @property
    def content(self):
        return self.__content
    
    @content.setter
    def content(self,content):
        return self.__content
    
    @property
    def language(self):
        return self.__language
    
    @language.setter
    def language(self, language):
        return self.__language

    @abstractmethod
    @staticmethod
    def from_json_object(content):
        pass

    @abstractmethod
    def to_json_object(self):
        pass


class Joke():
    def __init__(self, id=None, ref_id=None, is_edit=False,
                 difficulty=1, content="Haha", explanation=None,
                 language="english"):
        self.id=id
        self.ref_id=ref_id
        self.is_edit=is_edit
        self.difficulty=difficulty
        self.content=content 
        self.explanation=explanation 
        self.language=language

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id):
        """
        """
        if id 