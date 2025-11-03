# house all entity classes
from abc import ABC, abstractmethod
from datetime import date

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
        self.__id=id
    
    @property
    def ref_id(self):
        return self.__ref_id
    
    @ref_id.setter 
    def ref_id(self,ref_id):
        self.__ref_id=ref_id
    
    @property
    def is_edit(self):
        return self.__is_edit
    
    @is_edit.setter
    def is_edit(self, is_edit):
        if is_edit==True and self.ref_id == None:
            raise ValueError("Reference ID is required for edits")
        else:
            self.__is_edit=is_edit
    
    @property
    def language(self):
        return self.__language
    
    @language.setter
    def language(self, language):
        if language is None:
            raise ValueError("Language can not be none")
        elif not isinstance(language, str):
            raise ValueError("Language must be a string")
        else:
            self.__language=language

    @staticmethod
    @abstractmethod
    def from_json_object(content):
        pass

    @abstractmethod
    def to_json_object(self):
        pass


class Joke(BaseRecord):
    def __init__(self, id=None, ref_id=None, is_edit=False,
                 difficulty=1, content={"type":"one_liner","text": "Haha"}, explanation=None,
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
        if difficulty is None:
            raise ValueError("Difficulty level is required")
        elif not isinstance(difficulty, int):
            raise ValueError("Difficulty must be an integer")
        elif difficulty not in [1,2,3]:
            raise ValueError("Difficulty must be either 1,2, or 3")
        else:
            self.__difficulty=difficulty
    
    @property
    def content(self):
        return self.__content
    
    @content.setter
    def content(self, content):
        if not isinstance(content, dict):
            raise ValueError("Content must be a dictionary")
        elif "type" not in content:
            raise ValueError("Missing required fields")
        elif content["type"] not in ["one_liner", "qa"]:
            raise ValueError("Not a valid type")
        elif content["type"]=="one_liner":
            if "text" not in content:
                raise ValueError("Missing text field for one liner joke")
            if content["text"] is None:
                raise ValueError("One liner joke text field cannot be none")
            elif not isinstance(content["text"], str):
                raise ValueError("One liner joke text must be a string")
        elif content["type"]=="qa":
            if not all(key in content for key in ["question", "answer"]):
                raise ValueError("Missing required fields")
            elif not isinstance(content["question"],str):
                raise ValueError("Question for joke must be a string")
            elif not isinstance(content["answer"], str):
                raise ValueError("Answer for joke must be a string")
        else:
            self.__content=content
    
    @property
    def explanation(self):
        return self.__explanation
    
    @explanation.setter
    def explanation(self, explanation):
        if self.difficulty in [2,3]:
            if explanation is None:
                raise ValueError("Explanation cannot be none when difficulty is 2 or 3")
            elif not isinstance(explanation, str):
                raise ValueError("Explanation must be string")
            elif len(explanation.strip()) == 0:
                raise ValueError("Explanation cannot be empty")
        elif not isinstance(explanation, str) and not isinstance(explanation, type(None)):
            raise ValueError("Not the proper explanation type")
        else:
            self.__explanation=explanation
    
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
        if not isinstance(question, str):
            raise ValueError("Trivia question must be a string")
        else: 
            self.__question=question
    
    @property
    def answer(self):
        return self.__answer
    
    @answer.setter
    def answer(self,answer):
        if not isinstance(answer, str):
            raise ValueError("Trivia answer must be a string")
        else:
            self.__answer=answer

    @staticmethod
    def from_json_object(content):
        pass

    def to_json_object(self):
        pass

    
class Quotes(BaseRecord):
    def __init__(self, id, ref_id, is_edit, category, author, used_status="hey", language="english" ):
        super().__init__(id,ref_id,is_edit,language)
        self.category=category
        self.author=author
        self.used_status=used_status

    @property
    def category(self):
        return self.__category
    
    @category.setter
    def category(self, category):
        if not isinstance(category, str):
            raise ValueError("Category must be a string")
        else:
            self.__category=category
    
    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, author):
        if not isinstance(author, str):
            raise ValueError("Author must be a string")
        else:
            self.__author=author
    
    @property
    def used_status(self):
        return self.__used_status
    
    @used_status.setter
    def used_status(self, used_status):
        if not isinstance(used_status, str):
            raise ValueError("Used Status variable must be a string")
        else:
            self.__used_status=used_status
    
    @staticmethod
    def from_json_object(content):
        pass

    def to_json_object(self):
        pass

class Bios(BaseRecord):
    def __init__(self, id, ref_id, is_edit, language, birth_year, death_year, name, paragraph, summary, source_url ):
        super().__init__(id,ref_id,is_edit,language)
        self.birth_year=birth_year
        self.death_year=death_year
        self.name=name
        self.paragraph=paragraph
        self.summary=summary
        self.source_url=source_url

    @property
    def birth_year(self):
        return self.__birth_year
    
    @birth_year.setter
    def birth_year(self, birth_year):
        if not isinstance(birth_year, int) and not isinstance(birth_year,type(None)):
            raise ValueError("Birth year must be integer or None")
        if isinstance(birth_year, int):
            if birth_year > date.today().year:
                raise ValueError("Invalid year")
        else:
            self.__birth_year=birth_year

    @property
    def death_year(self):
        return self.__death_year
    
    @death_year.setter
    def death_year(self, death_year):
        if not isinstance(death_year, int) and not isinstance(death_year,type(None)):
            raise ValueError("Birth year must be integer or None")
        if isinstance(death_year, int):
            if death_year > date.today().year:
                raise ValueError("Invalid year")
        else:
            self.__death_year=death_year

    @property
    def name(self):
        return self.__name 
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ValueError("Author of bio's name must be a string")
        else:
            self.__name=name 

    @property
    def paragraph(self):
        return self.__paragraph
    
    @paragraph.setter
    def pragraph(self, paragraph):
        self.__paragraph=paragraph
        
    @staticmethod
    def from_json_object(content):
        pass

    def to_json_object(self):
        pass