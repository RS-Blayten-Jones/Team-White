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

# ----- Tests for Json Method Objects -----

class TestJokeJsonMethods:

    # --- Tests for from_json_object ---
    def test_from_json_object_valid(self):
        content = {
            "level": 2,
            "content": {"type": "one_liner", "text": "Funny joke"},
            "language": "english",
            "id": "1" * 24,
            "original_id": "2" * 24,
            "is_edit": True,
            "explanation": "Because it's clever"
        }
        joke = Joke.from_json_object(content)
        assert isinstance(joke, Joke)
        assert joke.difficulty == 2
        assert joke.content == {"type": "one_liner", "text": "Funny joke"}
        assert joke.language == "english"
        assert joke.id == "1" * 24
        assert joke.ref_id == "2" * 24
        assert joke.is_edit is True
        assert joke.explanation == "Because it's clever"

    @pytest.mark.parametrize("invalid_content", [
        "not a dict",  # Not a dictionary
        {"mesg": "Error message"},  # Contains error_field
        {"level": 1, "language": "english"},  # Missing 'content'
        {"level": 1, "content": "not a dict", "language": "english"}  # Content not dict
    ])
    def test_from_json_object_invalid(self, invalid_content):
        with pytest.raises(ValueError):
            Joke.from_json_object(invalid_content)

    def test_from_json_object_missing_optional_fields(self):
        content = {
            "level": 1,
            "content": {"type": "one_liner", "text": "Simple joke"},
            "language": "english"
        }
        joke = Joke.from_json_object(content)
        assert joke.id is None
        assert joke.ref_id is None
        assert joke.is_edit is None
        assert joke.explanation == ""  # Default from __init__


    # ---- Tests for to_json_object ----
    def test_to_json_object_valid(self):
        joke = Joke(difficulty=3, content={"type": "qa", "question": "Why?", "answer": "Because"},explanation = "Hard joke explanation", language="english")
        joke.id = "1" * 24
        joke.ref_id = "2" * 24
        joke.is_edit = False

        result = joke.to_json_object()
        assert isinstance(result, dict)
        assert result["level"] == 3
        assert result["content"] == {"type": "qa", "question": "Why?", "answer": "Because"}
        assert result["language"] == "english"
        assert result["explanation"] == "Hard joke explanation"
        assert result["id"] == "1" * 24
        assert result["original_id"] == "2" * 24
        assert result["is_edit"] is False

    def test_to_json_object_missing_optional_fields(self):
        joke = Joke(difficulty=1, content={"type": "one_liner", "text": "Quick joke"}, language="english")
        result = joke.to_json_object()
        assert "id" not in result
        assert "original_id" not in result
        assert "is_edit" not in result
