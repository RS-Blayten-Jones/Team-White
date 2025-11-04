from all_the_buzz.entities import Joke
import pytest

"""
This file runs unit tests on setter methods for Joke entities in: all_the_buzz/entities/record_entities.py
"""

# ----- Test for initalizing valid qa and one_liner Joke entitities -----
def test_valid_qa_joke():
    id_hex_str = "1" * 24
    ref_id_hex_str = "2" * 24
    joke = Joke(id=id_hex_str, ref_id=ref_id_hex_str, is_edit=False, language="english")
    joke.difficulty = 2
    joke.content = {"type": "qa", "question": "Why?", "answer": "Because"}
    joke.explanation = None

    assert joke.difficulty == 2
    assert joke.content["type"] == "qa"
    assert joke.content["question"] == "Why?"
    assert joke.content["answer"] == "Because"
    assert joke.explanation == None

def test_valid_one_liner_joke():
    id_hex_str = "1" * 24
    ref_id_hex_str = "2" * 24
    joke = Joke(id=id_hex_str, ref_id=ref_id_hex_str, is_edit=False, language="english")
    joke.difficulty = 2
    joke.content = {"type": "one_liner", "text": "This is a one-liner"}
    joke.explanation = None

    assert joke.difficulty == 2
    assert joke.content["type"] == "one_liner"
    assert joke.content["text"] == "This is a one-liner"
    assert joke.explanation == None

# ----- Test difficulty setters -----
def test_invalid_joke_difficulty_None():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Difficulty level is required"):
        joke.difficulty = None

def test_invalid_joke_difficulty_type():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Difficulty must be an integer"):
        joke.difficulty = "2"

def test_invalid_joke_difficulty_level():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Difficulty must be either 1, 2, or 3"):
        joke.difficulty = 4

# ----- Test content setters -----
def test_invalid_content_type():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Content must be a dictionary"):
        joke.content = "This is not a dictionary"

def test_content_missing_type():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Joke content missing required fields"):
        joke.content = {"question": "Why?", "answer": "Because"}

def test_content_invalid_type():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Not a valid type"):
        joke.content = {"type": "Wrong type", "question": "Why?", "answer": "Because"}

def test_content_one_liner_text_missing():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Missing text field for one liner joke"):
        joke.content = {"type": "one_liner"}

def test_content_one_liner_text_None():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="One liner joke text field cannot be none"):
        joke.content = {"type": "one_liner", "text" : None}

def test_content_one_liner_text_invalid_type():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="One liner joke text must be a string"):
        joke.content = {"type": "one_liner", "text" : 1234}

def test_content_qa_missing_question():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Missing required fields"):
        joke.content = {"type": "qa", "answer": "This is an answer"}

def test_content_qa_missing_answer():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Missing required fields"):
        joke.content = {"type": "qa", "question":"This is a question"}

def test_content_qa_invalid_question_type():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Question for joke must be a string"):
        joke.content = {"type": "qa", "question": 1234, "answer": "This is an answer"}

def test_content_qa_invalid_answer_type():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Answer for joke must be a string"):
        joke.content = {"type": "qa", "question": "This is a question", "answer": 1234}

def test_content_qa_question_empty_string():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Joke must have a question"):
        joke.content = {"type": "qa", "question": "", "answer": "This is an answer"}

def test_content_qa_answer_empty_string():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Joke must have an answer"):
        joke.content = {"type": "qa", "question": "This is a question", "answer": ""}

# ----- Test explanation setters -----
def test_invalid_explanation_type():
    joke = Joke(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    joke.difficulty = 3
    joke.content = {"type": "qa", "question": "Why?", "answer": "Because"}
    with pytest.raises(ValueError, match="Not the proper explanation type"):
        joke.explanation = 1234

def test_empty_explanation_for_difficulty_3():
    joke = Joke(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    joke.difficulty = 3
    joke.content = {"type": "qa", "question": "Why?", "answer": "Because"}
    
    with pytest.raises(ValueError, match="Jokes must have an explanation when difficulty is 3"):
        joke.explanation = ""

def test_None_explanation_for_difficulty_3():
    joke = Joke(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    joke.difficulty = 3
    joke.content = {"type": "qa", "question": "Why?", "answer": "Because"}
    
    with pytest.raises(ValueError, match="Jokes must have an explanation when difficulty is 3"):
        joke.explanation = None