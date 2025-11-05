import pytest
from datetime import datetime
from all_the_buzz.entities import Quotes

"""
Unit tests for Quotes entity setter methods.
python -m pytest --cov=all_the_buzz/entities --cov-report=term-missing
"""

# ----- Test for initializing a valid Quotes entity -----
def test_valid_quote():
    quote = Quotes(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
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
    quote = Quotes()
    with pytest.raises(ValueError, match="Category must be a string"):
        quote.category = 123  # invalid type

def test_category_lowercase():
    quote = Quotes()
    quote.category = "Science"
    assert quote.category == "science"

# ----- Test content setter -----
def test_invalid_content_type():
    quote = Quotes()
    with pytest.raises(ValueError, match="Quote content must be a string"):
        quote.content = 123

def test_empty_content():
    quote = Quotes()
    with pytest.raises(ValueError, match="Quote content cannot be empty"):
        quote.content = "   "

def test_content_too_long():
    quote = Quotes()
    with pytest.raises(ValueError, match="Quote content is too many characters"):
        quote.content = "a" * 1001

def test_valid_content():
    quote = Quotes()
    quote.content = "Short quote"
    assert quote.content == "Short quote"

# ----- Test author setter -----
def test_invalid_author_type():
    quote = Quotes()
    with pytest.raises(ValueError, match="Author must be a string"):
        quote.author = 456
def test_valid_author():
    quote = Quotes()
    quote.author = "Jane Doe"
    assert quote.author == "Jane Doe"

# ----- Test used_date setter -----
def test_invalid_used_date_type():
    quote = Quotes()
    with pytest.raises(ValueError, match="Used Status variable must be a string"):
        quote.used_date = 123

def test_invalid_used_date_format():
    quote = Quotes()
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
    quote = Quotes()
    quote.used_date = date_input
    assert quote.used_date == expected
