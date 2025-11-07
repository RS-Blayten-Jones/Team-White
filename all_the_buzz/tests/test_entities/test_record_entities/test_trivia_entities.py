# Copyright (C) 2025 Team White 
# Licensed under the MIT License
# See LICENSE for more details

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

class TestTriviaJsonMethods:

    # --- Tests for from_json_object ---
    def test_from_json_object_valid(self):
        content = {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "language": "english",
            "id": "2" *24,
            "original_id": "2" *24,
            "is_edit": True
        }
        trivia = Trivia.from_json_object(content)
        assert isinstance(trivia, Trivia)
        assert trivia.question == "What is the capital of France?"
        assert trivia.answer == "Paris"
        assert trivia.language == "english"
        assert trivia.id == "2" *24
        assert trivia.ref_id == "2" *24
        assert trivia.is_edit is True

    def test_from_json_object_missing_optional_fields(self):
        content = {
            "question": "Who wrote Hamlet?",
            "answer": "Shakespeare",
            "language": "english"
        }
        trivia = Trivia.from_json_object(content)
        assert trivia.id is None
        assert trivia.ref_id is None
        assert trivia.is_edit is None

    @pytest.mark.parametrize("invalid_content", [
        "not a dict",  # Not a dictionary
        {"mesg": "Error occurred"},  # Contains error_field
        {"question": "Q", "language": "english"},  # Missing 'answer'
    ])
    def test_from_json_object_invalid(self, invalid_content):
        with pytest.raises(ValueError):
            Trivia.from_json_object(invalid_content)

    # --- Tests for to_json_object ---
    def test_to_json_object_valid(self):
        trivia = Trivia(question="What is 2+2?", answer="4", language="english")
        trivia.id = "1" *24
        trivia.ref_id = "2" *24
        trivia.is_edit = False

        result = trivia.to_json_object()
        assert isinstance(result, dict)
        assert result["question"] == "What is 2+2?"
        assert result["answer"] == "4"
        assert result["language"] == "english"
        assert result["id"] == "1" *24
        assert result["original_id"] == "2" *24
        assert result["is_edit"] is False

    def test_to_json_object_missing_optional_fields(self):
        trivia = Trivia(question="What is the largest planet?", answer="Jupiter", language="english")
        result = trivia.to_json_object()
        assert "id" not in result
        assert "original_id" not in result
        assert "is_edit" not in result

    # --- Round-trip test ---
    def test_round_trip_json_methods(self):
        original_dict = {
            "question": "What is the speed of light?",
            "answer": "299,792 km/s",
            "language": "english"
        }
        trivia = Trivia.from_json_object(original_dict)
        new_dict = trivia.to_json_object()
        # Optional fields missing, so compare required ones
        for key in ["question", "answer", "language"]:
            assert new_dict[key] == original_dict[key]