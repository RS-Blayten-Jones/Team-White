from all_the_buzz.entities import Joke
import pytest


# Set up testing for Joke setters

# ----- Test for initalizing valid Joke entity -----
def test_joke_setter_valid():
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
    with pytest.raises(ValueError, match="Missing required fields"):
        joke.content = {"question": "Why?", "answer": "Because"}

def test_content_invalid_type():
    joke = Joke(id="1" * 24, ref_id="2" * 24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Not a valid type"):
        joke.content = {"type": "Wrong type", "question": "Why?", "answer": "Because"}
# ----- Test explanation setters -----
