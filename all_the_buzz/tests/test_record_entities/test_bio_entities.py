import pytest
from datetime import date
from all_the_buzz.entities import Bios

"""
Unit tests for Bios entity setter methods.
"""

# ----- Test valid initialization -----
def test_valid_bios():
    bio = Bios(id="1"*24, ref_id="2"*24, is_edit=False, language="English")
    bio.birth_year = 1879
    bio.death_year = 1955
    bio.name = "Albert Einstein"
    bio.paragraph = "A famous physicist."
    bio.summary = "Developed the theory of relativity."
    bio.source_url = "https://example.com"

    assert bio.birth_year == 1879
    assert bio.death_year == 1955
    assert bio.name == "Albert Einstein"
    assert bio.paragraph == "A famous physicist."
    assert bio.summary == "Developed the theory of relativity."
    assert bio.source_url == "https://example.com"

# ----- Test birth_year setter -----
def test_invalid_birth_year_type():
    bio = Bios()
    with pytest.raises(ValueError, match="Birth year must be integer or None"):
        bio.birth_year = "1990"

def test_invalid_birth_year_future():
    bio = Bios()
    future_year = date.today().year + 1
    with pytest.raises(ValueError, match="Invalid year"):
        bio.birth_year = future_year

def test_valid_birth_year_none():
    bio = Bios()
    bio.birth_year = None
    assert bio.birth_year is None

# ----- Test death_year setter -----
def test_invalid_death_year_type():
    bio = Bios()
    with pytest.raises(ValueError, match="Death year must be integer or None"):
        bio.death_year = "2020"

def test_invalid_death_year_future():
    bio = Bios()
    future_year = date.today().year + 1
    with pytest.raises(ValueError, match="Invalid year"):
        bio.death_year = future_year

def test_valid_death_year_none():
    bio = Bios()
    bio.death_year = None
    assert bio.death_year is None

# ----- Test name setter -----
def test_invalid_name_type():
    bio = Bios()
    with pytest.raises(ValueError, match="Author of bio's name must be a string"):
        bio.name = 123

def test_valid_name():
    bio = Bios()
    bio.name = "Marie Curie"
    assert bio.name == "Marie Curie"

# ----- Test paragraph setter -----
def test_invalid_paragraph_type():
    bio = Bios()
    with pytest.raises(ValueError, match="Bios paragraph must be a string"):
        bio.paragraph = 456

def test_valid_paragraph():
    bio = Bios()
    bio.paragraph = "This is a biography paragraph."
    assert bio.paragraph == "This is a biography paragraph."

# ----- Test summary setter -----
def test_invalid_summary_type():
    bio = Bios()
    with pytest.raises(ValueError, match="Bios summary must be a string"):
        bio.summary = 789

def test_valid_summary():
    bio = Bios()
    bio.summary = "Short summary."
    assert bio.summary == "Short summary."

# ----- Test source_url setter -----
def test_source_url_none():
    bio = Bios()
    with pytest.raises(ValueError, match="Source URL cannot be none"):
        bio.source_url = None

def test_source_url_invalid_type():
    bio = Bios()
    with pytest.raises(ValueError, match="Source URL must be a string"):
        bio.source_url = 123

def test_source_url_invalid_format():
    bio = Bios()
    with pytest.raises(ValueError, match="Invalid url"):
        bio.source_url = "not-a-url"

def test_valid_source_url():
    bio = Bios()
    bio.source_url = "https://valid-url.com"
    assert bio.source_url == "https://valid-url.com"