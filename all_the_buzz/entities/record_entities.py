# house all entity classes
from abc import ABC, abstractmethod
from datetime import date
from datetime import datetime
import validators
"""
record_entities.py

This module contains entity classes for records.

Classes:
    BaseRecord: An abstract class that all other record entities inherit from
    Joke: An entity class for storing and validating joke records
    Trivia: An entity class for storing and validating trivia records
    Quotes: An entity class for storing and validating quotes
    Bios: An entity class for storing and validating bio records
    """
class BaseRecord(ABC):
    """
    Abstract record entity class. All other classes
    inherit from it. This class includes all shared
    fields and methods include id, ref_id, is_edit, and
    language. 
    """
    def __init__(self, id=None, ref_id=None, is_edit=None,
                  language="english"):
        self.id=id
        self.ref_id=ref_id
        self.is_edit=is_edit
        self.language=language

    def hexadecimal_test(self, s):
        """
        Method for validating a string is 
        hexadecimal.This will be used for 
        validating mongodb ids.
        
        Args:
            s: a string 

        Returns:
            True if s is hexadecimal
            False if s is not hexadecimal

        Exceptions:
            ValueError: String is not hexadecimal
        """
        try:
            int(s,16)
            return True
        except ValueError:
            return False
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id):
        """
        Validates the document ID is proper format 
        based on mongodb ID.
        
        Exceptions:
            ValueError: ID is not stirng or None
            ValueError: ID is a string but not equal to 24 characters
            ValueError: ID is a string but not hexadecimal
            """
        #only hexadecimal characters and only 24 characters
        if not isinstance(id, str) and not isinstance(id, type(None)):
            raise ValueError("Record ID must be either string or None")
        elif isinstance(id, str) and len(id) != 24:
            raise ValueError("Invalid Record ID")
        elif isinstance(id, str) and not self.hexadecimal_test(id):
            raise ValueError("Invalid Record ID")
        else:
            self.__id=id
    
    @property
    def ref_id(self):
        return self.__ref_id
    
    @ref_id.setter 
    def ref_id(self,ref_id):
        """
        Validates the reference ID is in the proper
        format. 
        
        Exceptions:
            ValueError: Ref ID is not stirng or None
            ValueError: Ref ID is a string but not equal to 24 characters
            ValueError: Ref ID is a string but not hexadecimal
            """
        if not isinstance(ref_id, str) and not isinstance(ref_id, type(None)):
            raise ValueError("Reference ID must be either string or None")
        elif isinstance(ref_id, str) and len(ref_id) != 24:
            raise ValueError("Invalid Record ID")
        elif isinstance(ref_id, str) and not self.hexadecimal_test(ref_id):
            raise ValueError("Invalid Record ID")
        else:
            self.__ref_id=ref_id
    
    @property
    def is_edit(self):
        return self.__is_edit
    
    @is_edit.setter
    def is_edit(self, is_edit):
        """
        Validates proper fields are not missing if
        record is a proposed edit.
        
        Exception:
            ValueError: Reference ID is None
            """
        if is_edit==True and self.ref_id == None:
            raise ValueError("Reference ID is required for edits")
        else:
            self.__is_edit=is_edit
    
    @property
    def language(self):
        return self.__language
    
    @language.setter
    def language(self, language):
        """
        Validates the language is in the proper format.
        
        Exceptions:
            ValueError: Language cannot be None
            ValueError: Language must be a string
            """
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
    """
    Validates joke record data passed to it. This class
    includes id, ref_id, is_edit, difficulty, content,
    explanation, language
    
    To initilize this class, the from_json_object method can 
    be used. 

    The fields: 'level', 'content', 'language' are all required.
    """
    def __init__(self, id=None, ref_id=None, is_edit=None,
                 difficulty=1, content={"type":"one_liner","text": "Haha"}, explanation="",
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
        """
        Validates the difficulty is in the correct format.
        
        Exceptions:
            ValueError: Difficulty level is required
            ValueError: Difficulty must be an integer
            ValueError: Difficulty must be either 1,2, or 3
            """
        if difficulty is None:
            raise ValueError("Difficulty level is required")
        elif not isinstance(difficulty, int):
            raise ValueError("Difficulty must be an integer")
        elif difficulty not in [1,2,3]:
            raise ValueError("Difficulty must be either 1, 2, or 3")
        
        self.__difficulty=difficulty
    
    @property
    def content(self):
        return self.__content
    
    @content.setter
    def content(self, content):
        """
        Validates content follows the correct format
        
        Exceptions:
            ValueError: Content must be a dictionary
            ValueError: Type key must be in content
            ValueError: Type must either be one_liner or qa
            ValueError: If type one_liner, text must be in content
            ValueError: Text must not be none
            ValueError: Text must be a string
            ValueError: If type qa, question and answer must be in content
            ValueError: Question must be a string
            ValueError: Answer must be a string
            """
        if not isinstance(content, dict):
            raise ValueError("Content must be a dictionary")
        elif "type" not in content:
            raise ValueError("Joke content missing required fields")
        
        # Content type One liners
        elif content["type"] not in ["one_liner", "qa"]:
            raise ValueError("Not a valid type")
        elif content["type"]=="one_liner":
            if "text" not in content:
                raise ValueError("Missing text field for one liner joke")
            if content["text"] is None:
                raise ValueError("One liner joke text field cannot be none")
            elif not isinstance(content["text"], str):
                raise ValueError("One liner joke text must be a string")
            
        # Content type QA
        elif content["type"]=="qa":
            if not all(key in content for key in ["question", "answer"]):
                raise ValueError("Missing required fields")
            elif not isinstance(content["question"],str):
                raise ValueError("Question for joke must be a string")
            elif len((content["question"].strip())) == 0:
                raise ValueError("Joke must have a question")
            elif not isinstance(content["answer"], str):
                raise ValueError("Answer for joke must be a string")
            elif len((content["answer"].strip())) == 0:
                raise ValueError("Joke must have an answer")
        self.__content=content
    
    @property
    def explanation(self):
        return self.__explanation
    
    @explanation.setter
    def explanation(self, explanation):
        """
        Validates explanation is in the proper format.
        
        Exceptions:
            ValueError: Explaination is not the proper type
            ValueError: Joke must have explanation when difficulty 3
            """
        if not isinstance(explanation, str) and not isinstance(explanation, type(None)):
            raise ValueError("Not the proper explanation type")
        elif (explanation is None or len(explanation.strip()) == 0) and self.difficulty == 3:
            raise ValueError("Jokes must have an explanation when difficulty is 3")
        self.__explanation=explanation
    
    @staticmethod
    def from_json_object(content):
        """
        Method for converting json string to Joke object.
        
        Excpetions: 
            ValueError: Not proper format
            ValueError: Missing required fields
            ValueError: Content not in dictionary format
            """
        requried_fields=['level', 'content', 'language']
        error_field='mesg'
        if not isinstance(content, dict):
            raise ValueError("Must be dictionary input")
        elif error_field in content:
            raise ValueError(content[error_field])
        elif not all(key in content for key in requried_fields):
            raise ValueError("Missing required fields")
        elif not isinstance(content['content'], dict):
            raise ValueError("Content must be a dictionary")
        else:
            joke_object=Joke(difficulty=content['level'], content=content['content'], 
                        language=content["language"])
            if "id" in content:
                joke_object.id=content["id"] 
            if "original_id" in content:
                joke_object.ref_id=content["original_id"]
            if "is_edit" in content:
                joke_object.is_edit=content["is_edit"]
            if "explanation" in content:
                joke_object.explanation=content["explanation"]
            return joke_object
                

    def to_json_object(self):
        """"
        Method for converting Joke object to dict.
        """
        record_dict={"level": self.difficulty, "content": self.content, "explanation": self.explanation,
                 "language":self.language}
        if self.id is not None:
            record_dict["id"]= self.id
        if self.ref_id is not None:
            record_dict["original_id"]=self.ref_id
        if self.is_edit is not None:
            record_dict["is_edit"]=self.is_edit

        return record_dict

#joke=Joke.from_json_object(content)
#joke.to_json_object()


class Trivia(BaseRecord):
    """
    Validates trivia record data passed to it. This class
    includes id, ref_id, is_edit, question, answer, language
    
    To initilize this class, the from_json_object method can 
    be used. 

    The fields: 'question', 'answer', 'language' are all required.
    """
    def __init__(self, id=None, ref_id=None, is_edit=None, question="Question", answer="Answer", language="english"):
        super().__init__(id,ref_id,is_edit,language)
        self.question=question
        self.answer=answer

    @property
    def question(self):
        return self.__question
    
    @question.setter
    def question(self,question):
        """
        Validates question is in the proper format.
        
        Exceptions:
            ValueError: Question must be a string
            """
        if not isinstance(question, str):
            raise ValueError("Trivia question must be a string")
        elif len(question.strip()) == 0:
            raise ValueError("Trivia question cannot be blank")
        elif len(question) > 1000:
            raise ValueError("Trivia question too long")
        self.__question=question
    
    @property
    def answer(self):
        return self.__answer
    
    @answer.setter
    def answer(self,answer):
        """
        Validates answer is in the proper format.
        
        Exceptions:
            ValueError: Answer must be a string
            """
        if not isinstance(answer, str):
            raise ValueError("Trivia answer must be a string")
        elif len(answer) > 1000:
            raise ValueError("Trivia answer too long")
        self.__answer=answer

    @staticmethod
    def from_json_object(content):
        """
        Method for converting json string to Trivia object.
        
        Excpetions: 
            ValueError: Not proper format
            ValueError: Missing required fields
            """
        requried_fields=['question', 'answer','language']
        error_field='mesg'
        if not isinstance(content, dict):
            raise ValueError("Must be dictionary input")
        elif error_field in content:
            raise ValueError(content[error_field])
        elif not all(key in content for key in requried_fields):
            raise ValueError("Missing required fields")
        else:
            trivia_object=Trivia(question=content["question"], answer=content["answer"], 
                        language=content["language"])
            if "id" in content:
                trivia_object.id=content["id"] 
            if "original_id" in content:
                trivia_object.ref_id=content["original_id"]
            if "is_edit" in content:
                trivia_object.is_edit=content["is_edit"]
            return trivia_object
                

    def to_json_object(self):
        """"
        Method for converting Trivia object to dict.
        """
        record_dict={"question": self.question, "answer": self.answer, 
                 "language":self.language}
        if self.id is not None:
            record_dict["id"]= self.id
        if self.ref_id is not None:
            record_dict["original_id"]=self.ref_id
        if self.is_edit is not None:
            record_dict["is_edit"]=self.is_edit

        return record_dict

    
class Quotes(BaseRecord):
    """
    Validates quotes record data passed to it. This class
    includes id, ref_id, is_edit, category, author, used_status,
    language
    
    To initilize this class, the from_json_object method can 
    be used. 

    The fields: 'content','author', 'language' are all required.
    """
    def __init__(self, id=None, ref_id=None, is_edit=None, category="category",
                 content="stuff",author="Joe", used_date="03/15/2020", language="english" ):
        super().__init__(id,ref_id,is_edit,language)
        self.category=category
        self.content=content
        self.author=author
        self.used_date=used_date
#TODO: fix used date string mm-dd-yyyy
    @property
    def category(self):
        return self.__category
    
    @category.setter
    def category(self, category):
        """
        Validates category is proper format.
        
        Exceptions:
            ValueError: Category must be a string
            """
        if not isinstance(category, str):
            raise ValueError("Category must be a string")
        else:
            self.__category=category.lower()

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self,content):
        """
        Validates content is proper format

        Exceptions:
            ValueError: Content must be a string
            ValueError: Content is too many characters
        """
        if not isinstance(content, str):
            raise ValueError("Quote content must be a string")
        elif len(content.strip()) == 0:
            raise ValueError("Quote content cannot be empty")
        elif len(content) > 1000:
            raise ValueError("Quote content is too many characters")
        else:
            self.__content=content
            
    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, author):
        """
        Validates author is in proper format.
        
        Exceptions:
            ValueError: Author must be a string
            """
        if not isinstance(author, str):
            raise ValueError("Author must be a string")
        else:
            self.__author=author
    
    @property
    def used_date(self):
        return self.__used_date
    
    @used_date.setter
    def used_date(self, used_date):
        """
        Validates used_date is in correct format. 
        Dates passed will be reformatted to mm/dd/yyyy for consistency
        
        Exceptions:
            ValueError: Used date must be a string date
            in one of the possible formats
            """
        
        possible_formats = [
                "%Y-%m-%d",    # 2025-11-04
                "%m-%d-%Y",    # 11-04-2025
                "%m/%d/%Y",    # 11/04/2025
                "%d-%m-%Y",    # 04-11-2025
                "%d/%m/%Y",    # 04/11/2025
                "%m-%d-%y",    # 11-04-25
                "%d-%m-%y",    # 04-11-25
                "%m/%d/%y",    # 11/04/25
                "%d/%m/%y"     # 04/11/25
            ]

        if not isinstance(used_date, str):
            raise ValueError("Used Status variable must be a string")
        
        parsed_date = None
        for fmt in possible_formats:
            try:
                parsed_date = datetime.strptime(used_date.strip(), fmt)
                break
            except ValueError:
                continue
        
        if parsed_date is None:
            raise ValueError("Used Status must be a valid date string in a recognized format")

        self.__used_date = parsed_date.strftime("%m/%d/%Y")
        
    @staticmethod
    def from_json_object(content):
        """
        Method for converting json string to Quotes object.
        
        Excpetions: 
            ValueError: Not proper format
            ValueError: Missing required fields
            """
        requried_fields=['content', 'author', 'language']
        error_field='mesg'
        if not isinstance(content, dict):
            raise ValueError("Must be dictionary input")
        elif error_field in content:
            raise ValueError(content[error_field])
        elif not all(key in content for key in requried_fields):
            raise ValueError("Missing required fields")
        else:
            quotes_object=Quotes(content=content["content"], category=content["category"],
                                 author=content["author"],language=content["language"])
            if "id" in content:
                quotes_object.id=content["id"] 
            if "original_id" in content:
                quotes_object.ref_id=content["original_id"]
            if "is_edit" in content:
                quotes_object.is_edit=content["is_edit"]
            if "category" in content:
                quotes_object.category=content["category"]
            return quotes_object
                

    def to_json_object(self):
        """"
        Method for converting Trivia object to dict.
        """
        record_dict={"content": self.content, "author":self.author, 
                     "language":self.language}
        if self.id is not None:
            record_dict["id"]= self.id
        if self.ref_id is not None:
            record_dict["original_id"]=self.ref_id
        if self.is_edit is not None:
            record_dict["is_edit"]=self.is_edit
        if self.category is not None:
            record_dict["category"]=self.category
        return record_dict

class Bios(BaseRecord):
    """
    Validates bios record data passed to it. This class
    includes id, ref_id, is_edit, birth_year, death_year,
    paragraph, summary, source_url, language
    
    To initilize this class, the from_json_object method can 
    be used. 

    The fields: 'name','paragraph','language','source_url' are all required.
    """
    def __init__(self, id=None, ref_id=None, is_edit=None,
                    language="English", birth_year=0000, death_year=0000, name="Bob", 
                    paragraph="Bio stuff", summary="summary", source_url="https://fake-url.com" ):
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
        """
        Validates that birth year is in the proper format.
        
        Exceptions:
            ValueError: Birth year must be integer or None
            ValueError: Invalid year (future year)
            """
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
        """
        Validates death year is in proper format.
        
        Exception: 
            ValueError: Death year must be integer or None
            ValueError: Death year is invalid
            """
        if not isinstance(death_year, int) and not isinstance(death_year,type(None)):
            raise ValueError("Death year must be integer or None")
        if isinstance(death_year, int):
            if death_year > date.today().year: # check if year is in the past
                raise ValueError("Invalid year")
        else:
            self.__death_year=death_year

    @property
    def name(self):
        return self.__name 
    
    @name.setter
    def name(self, name):
        """"
        Validates name is in proper format.
        
        Exceptions:
            ValueError: Author name must be a string.
            """
        if not isinstance(name, str):
            raise ValueError("Author of bio's name must be a string")
        else:
            self.__name=name 

    @property
    def paragraph(self):
        return self.__paragraph
    
    @paragraph.setter
    def paragraph(self, paragraph):
        """
        Validates paragraph is in proper format.
        
        Exceptions:
            ValueError: Paragraph must be a string
            """
        if not isinstance(paragraph, str):
            raise ValueError("Bios paragraph must be a string")
        self.__paragraph=paragraph
    
    @property
    def summary(self):
        return self.__summary
    
    @summary.setter
    def summary(self, summary):
        """
        Validates summary is in the proper format.
        
        Exception:
            ValueError: Summary must be a string
            """
        if not isinstance(summary, str):
            raise ValueError("Bios summary must be a string")
        self.__summary=summary

    @property
    def source_url(self):
        return self.__source_url
    
    @source_url.setter
    def source_url(self, source_url):
        """"
        Validates source url is in proper format.
        
        Exception:
            ValueError: Source url cannot be none
            ValueError: Source url must be a string
            ValueError: URL is invalid
            """
        if source_url is None:
            raise ValueError("Source URL cannot be none")
        elif not isinstance(source_url, str):
            raise ValueError("Source URL must be a string")
        elif not validators.url(source_url):
            raise ValueError("Invalid url")
        else:
            self.__source_url=source_url

    @staticmethod
    def from_json_object(content):
        """
        Method for converting json string to Bios object.
        
        Excpetions: 
            ValueError: Not proper format
            ValueError: Missing required fields
            """
        requried_fields=['name','paragraph','language','source_url']
        error_field='mesg'
        if not isinstance(content, dict):
            raise ValueError("Must be dictionary input")
        elif error_field in content:
            raise ValueError(content[error_field])
        elif not all(key in content for key in requried_fields):
            raise ValueError("Missing required fields")
        else:
            bios_object=Bios(name=content["name"], paragraph=content["paragraph"],
                             source_url=content["source_url"],language=content["language"])
            if "id" in content:
                bios_object.id=content["id"] 
            if "original_id" in content:
                bios_object.ref_id=content["original_id"]
            if "is_edit" in content:
                bios_object.is_edit=content["is_edit"]
            if "birth_year" in content:
                bios_object.birth_year=content["birth_year"]
            if "death_year" in content:
                bios_object.death_year=content["death_year"]
            if "summary" in content:
                bios_object.summary=content["summary"]
            return bios_object
                
    def to_json_object(self):
        """"
        Method for converting Bios object to dict.
        """
        record_dict={"name":self.name, "paragraph": self.paragraph,
                     "source_url": self.source_url, "language":self.language}
        if self.id is not None:
            record_dict["id"]= self.id
        if self.ref_id is not None:
            record_dict["original_id"]=self.ref_id
        if self.is_edit is not None:
            record_dict["is_edit"]=self.is_edit
        if self.birth_year is not None:
            record_dict["birth_year"]=self.birth_year
        if self.death_year is not None:
            record_dict["death_year"]=self.death_year
        if self.summary is not None:
            record_dict["summary"]=self.summary
        return record_dict
    
