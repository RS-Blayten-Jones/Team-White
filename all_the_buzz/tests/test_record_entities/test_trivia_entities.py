from all_the_buzz.entities import Trivia
import pytest

"""
This file runs unit tests on setter methods for Trivia entities in: all_the_buzz/entities/record_entities.py
"""

# ----- Test for initalizing a valid Trivia entity -----
def test_valid_trivia():
    trivia = Trivia(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    trivia.question = "This is a question"
    trivia.answer = "This is an answer"

    assert trivia.question == "This is a question"
    assert trivia.answer == "This is an answer"

# ----- Test question setters -----
def test_invalid_question_type():
    trivia = Trivia(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Trivia question must be a string"):
        trivia.question = 1234

def test_invalid_question_empty():
    trivia = Trivia(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Trivia question cannot be blank"):
        trivia.question = ""

def test_question_too_long():
    trivia = Trivia(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    with pytest.raises(ValueError, match="Trivia question too long"):
        trivia.question = "1" * 1001

# ----- Test answer setters -----
def test_invalid_answer_type():
    trivia = Trivia(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    trivia.question = "This is a question"
    with pytest.raises(ValueError, match="Trivia answer must be a string"):
        trivia.answer = 1234

def test_answer_too_long():
    trivia = Trivia(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    trivia.question = "This is a question"
    with pytest.raises(ValueError, match="Trivia answer too long"):
        trivia.answer= "1" * 1001