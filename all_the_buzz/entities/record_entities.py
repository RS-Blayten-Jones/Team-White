# house all entity classes
from abc import ABC, abstractmethod

class BaseRecord(ABC):
    def __init__(self, id=None, ref_id=None, is_edit=False,
                  language="english"):
        self.id=id
        self.ref_id=ref_id
        self.is_edit=is_edit
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


class Joke(BaseRecord):
    def __init__(self, id=None, ref_id=None, is_edit=False,
                 difficulty=1, content={"joke":"haha"}, explanation=None,
                 language="english"):
        super().__init__(id,ref_id,is_edit,language)
        self.difficulty=difficulty
        self.content=content 
        self.explanation=explanation 
        
    @property
    def difficulty(self):
        return self.__difficulty
    
    @difficulty.setter
    def difficulty(self, difficulty):
        return self.__difficulty
    
    @property
    def content(self):
        return self.__content
    
    @content.setter
    def content(self, content):
        return self.__content
    
    @staticmethod
    def from_json_object(content):
        pass

    def to_json_object(self):
        pass
    
class Trivia(BaseRecord):
    def __init__(self, id, ref_id, is_edit, question, answer, language ):
        super().__init__(id,ref_id,is_edit,language)
        self.question=question
        self.answer=answer

    @property
    def question(self):
        return self.__question
    
    @question.setter
    def question(self,question):
        return self.__question
    
    @property
    def answer(self):
        return self.__answer
    
    @answer.setter
    def answer(self,answer):
        return self.__answer

    @staticmethod
    def from_json_object(content):
        pass

    def to_json_object(self):
        pass

    