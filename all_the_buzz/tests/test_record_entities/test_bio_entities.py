import pytest
from datetime import date
from all_the_buzz.entities import Bio

"""
Unit tests for Bio entity setter methods.
"""

# ----- Test valid initialization -----
def test_valid_Bio():
    bio = Bio(id="1"*24, ref_id="2"*24, is_edit=False, language="English")
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
    bio = Bio()
    with pytest.raises(ValueError, match="Birth year must be integer or None"):
        bio.birth_year = "1990"

def test_invalid_birth_year_future():
    bio = Bio()
    future_year = date.today().year + 1
    with pytest.raises(ValueError, match="Invalid year"):
        bio.birth_year = future_year

def test_valid_birth_year_none():
    bio = Bio()
    bio.birth_year = None
    assert bio.birth_year is None

# ----- Test death_year setter -----
def test_invalid_death_year_type():
    bio = Bio()
    with pytest.raises(ValueError, match="Death year must be integer or None"):
        bio.death_year = "2020"

def test_invalid_death_year_future():
    bio = Bio()
    future_year = date.today().year + 1
    with pytest.raises(ValueError, match="Invalid year"):
        bio.death_year = future_year

def test_valid_death_year_none():
    bio = Bio()
    bio.death_year = None
    assert bio.death_year is None

# ----- Test name setter -----
def test_invalid_name_type():
    bio = Bio()
    with pytest.raises(ValueError, match="Author of bio's name must be a string"):
        bio.name = 123

def test_valid_name():
    bio = Bio()
    bio.name = "Marie Curie"
    assert bio.name == "Marie Curie"

# ----- Test paragraph setter -----
def test_invalid_paragraph_type():
    bio = Bio()
    with pytest.raises(ValueError, match="Bio paragraph must be a string"):
        bio.paragraph = 456

def test_valid_paragraph():
    bio = Bio()
    bio.paragraph = "This is a biography paragraph."
    assert bio.paragraph == "This is a biography paragraph."

# ----- Test summary setter -----
def test_invalid_summary_type():
    bio = Bio()
    with pytest.raises(ValueError, match="Bio summary must be a string"):
        bio.summary = 789

def test_valid_summary():
    bio = Bio()
    bio.summary = "Short summary."
    assert bio.summary == "Short summary."

# ----- Test source_url setter -----
def test_source_url_none():
    bio = Bio()
    with pytest.raises(ValueError, match="Source URL cannot be none"):
        bio.source_url = None

def test_source_url_invalid_type():
    bio = Bio()
    with pytest.raises(ValueError, match="Source URL must be a string"):
        bio.source_url = 123

def test_source_url_invalid_format():
    bio = Bio()
    with pytest.raises(ValueError, match="Invalid url"):
        bio.source_url = "not-a-url"

def test_valid_source_url():
    bio = Bio()
    bio.source_url = "https://valid-url.com"
    assert bio.source_url == "https://valid-url.com"


class TestBioJsonMethods:

    # --- Tests for from_json_object ---
    def test_from_json_object_valid(self):
        content = {
            "name": "Albert Einstein",
            "paragraph": "Albert Einstein was a theoretical physicist.",
            "language": "English",
            "source_url": "https://example.com/einstein",
            "id": "1" * 24,
            "original_id": "2" * 24,
            "is_edit": True,
            "birth_year": 1879,
            "death_year": 1955,
            "summary": "Developed the theory of relativity."
        }
        bio = Bio.from_json_object(content)
        assert isinstance(bio, Bio)
        assert bio.name == content["name"]
        assert bio.paragraph == content["paragraph"]
        assert bio.language == content["language"]
        assert bio.source_url == content["source_url"]
        assert bio.id == "1" * 24
        assert bio.ref_id == "2" * 24
        assert bio.is_edit is True
        assert bio.birth_year == 1879
        assert bio.death_year == 1955
        assert bio.summary == content["summary"]

    def test_from_json_object_missing_optional_fields(self):
        content = {
            "name": "Marie Curie",
            "paragraph": "Marie Curie was a pioneering physicist and chemist.",
            "language": "English",
            "source_url": "https://example.com/curie"
        }
        bio = Bio.from_json_object(content)
        assert bio.id is None
        assert bio.ref_id is None
        assert bio.is_edit is None
        assert bio.birth_year == 1900  # default from __init__
        assert bio.death_year == 2020  # default from __init__
        assert bio.summary == "summary"  # default from __init__

    @pytest.mark.parametrize("invalid_content", [
        "not a dict",  # Not a dictionary
        {"mesg": "Error occurred"},  # Contains error_field
        {"name": "Ada Lovelace", "language": "English"}  # Missing 'paragraph' and 'source_url'
    ])
    def test_from_json_object_invalid(self, invalid_content):
        with pytest.raises(ValueError):
            Bio.from_json_object(invalid_content)

    # --- Tests for to_json_object ---
    def test_to_json_object_valid(self):
        bio = Bio(name="Nikola Tesla", paragraph="Inventor and engineer.", source_url="https://example.com/tesla")
        bio.id = "1" * 24
        bio.ref_id = "2" * 24
        bio.is_edit = False
        bio.birth_year = 1856
        bio.death_year = 1943
        bio.summary = "Known for AC electricity."

        result = bio.to_json_object()
        assert isinstance(result, dict)
        assert result["name"] == "Nikola Tesla"
        assert result["paragraph"] == "Inventor and engineer."
        assert result["source_url"] == "https://example.com/tesla"
        assert result["language"] == "English"
        assert result["id"] == "1" * 24
        assert result["original_id"] == "2" * 24
        assert result["is_edit"] is False
        assert result["birth_year"] == 1856
        assert result["death_year"] == 1943
        assert result["summary"] == "Known for AC electricity."

    def test_to_json_object_missing_optional_fields(self):
        bio = Bio(name="Isaac Newton", paragraph="Mathematician and physicist.", source_url="https://example.com/newton")
        result = bio.to_json_object()
        assert "id" not in result
        assert "original_id" not in result
        assert "is_edit" not in result
        assert "birth_year" in result  # defaults to 1900
        assert "death_year" in result  # defaults to 2020
        assert "summary" in result  # defaults to "summary"

    # --- Round-trip test ---
    def test_round_trip_json_methods(self):
        original_dict = {
            "name": "Leonardo da Vinci",
            "paragraph": "Renaissance artist and inventor.",
            "language": "English",
            "source_url": "https://example.com/davinci",
            "summary": "Painter of the Mona Lisa."
        }
        bio = Bio.from_json_object(original_dict)
        new_dict = bio.to_json_object()
        for key in ["name", "paragraph", "language", "source_url", "summary"]:
            assert new_dict[key] == original_dict[key]