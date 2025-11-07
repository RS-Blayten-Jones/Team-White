# Copyright (C) 2025 Team White 
# Licensed under the MIT License
# See LICENSE for more details

import pytest
from datetime import datetime
from all_the_buzz.entities import Quote

"""
Unit tests for Quote entity setter methods.
python -m pytest --cov=all_the_buzz/entities --cov-report=term-missing
"""

# ----- Test for initializing a valid Quote entity -----
def test_valid_quote():
    quote = Quote(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    quote.category = "Computer"
    quote.content = "Hello World!"
    quote.author = "Billy Bob"
    quote.used_date = "20-04-2025"

    assert quote.category == "computer"  # lowercased
    assert quote.content == "Hello World!"
    assert quote.author == "Billy Bob"
    assert quote.used_date == "04/20/2025"  # reformatted

# ----- Test category setter -----
def test_invalid_category_type():
    quote = Quote()
    with pytest.raises(ValueError, match="Category must be a string"):
        quote.category = 123  # invalid type

def test_category_lowercase():
    quote = Quote()
    quote.category = "Science"
    assert quote.category == "science"

# ----- Test content setter -----
def test_invalid_content_type():
    quote = Quote()
    with pytest.raises(ValueError, match="Quote content must be a string"):
        quote.content = 123

def test_empty_content():
    quote = Quote()
    with pytest.raises(ValueError, match="Quote content cannot be empty"):
        quote.content = "   "

def test_content_too_long():
    quote = Quote()
    with pytest.raises(ValueError, match="Quote content is too many characters"):
        quote.content = "a" * 1001

def test_valid_content():
    quote = Quote()
    quote.content = "Short quote"
    assert quote.content == "Short quote"

# ----- Test author setter -----
def test_invalid_author_type():
    quote = Quote()
    with pytest.raises(ValueError, match="Author must be a string"):
        quote.author = 456
def test_valid_author():
    quote = Quote()
    quote.author = "Jane Doe"
    assert quote.author == "Jane Doe"

# ----- Test used_date setter -----
def test_invalid_used_date_type():
    quote = Quote()
    with pytest.raises(ValueError, match="Used Status variable must be a string"):
        quote.used_date = 123

def test_invalid_used_date_format():
    quote = Quote()
    with pytest.raises(ValueError, match="Used Status must be a valid date string"):
        quote.used_date = "invalid-date"


@pytest.mark.parametrize("date_input,expected", [
    ("2025-11-04", "11/04/2025"),  # YYYY-MM-DD → Nov 4
    ("11-04-2025", "11/04/2025"),  # MM-DD-YYYY → Nov 4
    ("11/04/2025", "11/04/2025"),  # MM/DD/YYYY → Nov 4
    ("04-11-2025", "04/11/2025"),  # DD-MM-YYYY → Apr 11
    ("04/11/2025", "04/11/2025"),  # DD/MM/YYYY → Apr 11
    ("11-04-25", "11/04/2025"),    # MM-DD-YY → Nov 4
    ("04-11-25", "04/11/2025"),    # DD-MM-YY → Apr 11
    ("11/04/25", "11/04/2025"),    # MM/DD/YY → Nov 4
    ("04/11/25", "04/11/2025"),    # DD/MM/YY → Apr 11
])

def test_valid_used_date_formats(date_input, expected):
    quote = Quote()
    quote.used_date = date_input
    assert quote.used_date == expected


class TestQuoteJsonMethods:

    # --- Tests for from_json_object ---
    def test_from_json_object_valid(self):
        content = {
            "content": "The only limit to our realization of tomorrow is our doubts of today.",
            "author": "Franklin D. Roosevelt",
            "language": "english",
            "category": "inspiration",
            "id": "1" * 24,
            "original_id": "2" * 24,
            "is_edit": True
        }
        quote = Quote.from_json_object(content)
        assert isinstance(quote, Quote)
        assert quote.content == content["content"]
        assert quote.author == content["author"]
        assert quote.language == content["language"]
        assert quote.category == "inspiration"  # category is normalized
        assert quote.id == "1" * 24
        assert quote.ref_id == "2" * 24
        assert quote.is_edit is True

    def test_from_json_object_missing_optional_fields(self):
        content = {
            "content": "Life is what happens when you're busy making other plans.",
            "author": "John Lennon",
            "language": "english",
        }
        quote = Quote.from_json_object(content)
        assert quote.id is None
        assert quote.ref_id is None
        assert quote.is_edit is None
        assert quote.category == "category"  # default from __init__

    @pytest.mark.parametrize("invalid_content", [
        "not a dict",  # Not a dictionary
        {"mesg": "Error occurred"},  # Contains error_field
        {"content": "Quote text", "language": "english"}  # Missing 'author'
    ])
    def test_from_json_object_invalid(self, invalid_content):
        with pytest.raises(ValueError):
            Quote.from_json_object(invalid_content)

    # --- Tests for to_json_object ---
    def test_to_json_object_valid(self):
        quote = Quote(content="Stay hungry, stay foolish.", author="Steve Jobs", language="english")
        quote.id = "1" * 24
        quote.ref_id = "2" * 24
        quote.is_edit = False
        quote.category = "Motivation"

        result = quote.to_json_object()
        assert isinstance(result, dict)
        assert result["content"] == "Stay hungry, stay foolish."
        assert result["author"] == "Steve Jobs"
        assert result["language"] == "english"
        assert result["id"] == "1" * 24
        assert result["original_id"] == "2" * 24
        assert result["is_edit"] is False
        assert result["category"] == "motivation"  # normalized

    def test_to_json_object_missing_optional_fields(self):
        quote = Quote(content="Do or do not. There is no try.", author="Yoda", language="english")
        result = quote.to_json_object()
        assert "id" not in result
        assert "original_id" not in result
        assert "is_edit" not in result
        assert "category" in result  # category defaults to "category"

    # --- Round-trip test ---
    def test_round_trip_json_methods(self):
        original_dict = {
            "content": "Be yourself; everyone else is already taken.",
            "author": "Oscar Wilde",
            "language": "english",
            "category": "wisdom"
        }
        quote = Quote.from_json_object(original_dict)
        new_dict = quote.to_json_object()
        for key in ["content", "author", "language", "category"]:
            assert new_dict[key] == original_dict[key].lower() if key == "category" else original_dict[key]