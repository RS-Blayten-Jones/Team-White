# Copyright (C) 2025 Team White 
# Licensed under the MIT License
# See LICENSE for more details

"""
This file runs unit tests on setter methods for Credentials and Token entities in: all_the_buzz/entities/credentials_entity.py

To unit test:
(.venv)...\project-folder> pip install pytest
(.venv)...\project-folder> python -m pytest

To test coverage:
python -m pytest --cov=entities --cov-report=term
(.venv)...\project-folder> pip install pytest-cov
(.venv)...\project-folder> python -m pytest --cov=entities --cov-report=term
(.venv)...\project-folder> python -m pytest --cov=entities --cov-report=term-missing
"""  

from all_the_buzz.entities import Credentials, Token
import pytest

# ------- Testing ID setter ------
def test_id_setter_valid():
    cred = Credentials()
    cred.id = 1234
    assert cred.id == 1234

def test_id_setter_none():
    cred = Credentials()
    with pytest.raises(ValueError):
        cred.id = None

def test_id_setter_string():
    cred = Credentials()
    with pytest.raises(ValueError):
        cred.id = "1234"

def test_id_setter_negative():
    cred = Credentials()
    with pytest.raises(ValueError):
        cred.id = -1
    
# ------ Testing fName setter ------
def test_fName_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.fName = "Mike"
    assert cred.fName == "Mike"
    
# Test for allowing apostrophes in names
# def test_fName_setter_valid_apostrophe():
#     cred = Credentials()
#     cred.id = 1234
#     cred.fName ="De'Wayne"
#     pass

def test_fName_setter_none():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError, match="First name must be provided"):
        cred.fName = None

def test_fName_setter_int():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.fName = 1234

def test_fName_setter_length_zero():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.fName = ""

def test_fName_setter_spaces():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.fName = "           "

def test_fName_setter_greater_than_50():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.fName = "a" * 51
    
# def test_fName_setter_non_letters():
#     cred = Credentials()
#     cred.id = 1234
#     with pytest.raises(ValueError):
#         cred.fName = "$p3nc3r"

# ------ Testing lName setter ------
def test_lName_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.lName = "Jones"
    assert cred.lName == "Jones"

# Test for allowing apostrophes in names
# def test_lName_setter_valid_apostrophe():
#     cred = Credentials()
#     cred.id = 1234
#     cred.lName = "O'Conner"
#     assert cred.lName == "O'Conner"

def test_lName_setter_none():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lName = None

def test_lName_setter_int():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lName = 1234

def test_lName_setter_length_zero():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lName = ""

def test_lName_setter_spaces():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lName = "           "

def test_lName_setter_greater_than_50():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lName = "a" * 51

# def test_lName_setter_non_letters():
#     cred = Credentials()
#     cred.id = 1234
#     with pytest.raises(ValueError):
#         cred.lName = "$p3nc3r"

# ------ Testing dept setter ------
def test_dept_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.dept = "Sales"
    assert cred.dept == "Sales"

def test_dept_setter_none():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.dept = None

def test_dept_setter_int():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.dept = 1234

def test_dept_setter_length_zero():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.dept = ""

def test_dept_setter_spaces():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.dept = "       "

def test_dept_setter_greater_than_35():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.dept = "a" * 36

def test_dept_setter_non_letters():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.dept = "$4l3$"

# ------ Testing Title setter ------
def test_title_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.title = "Emperor of the Universe"
    assert cred.title == "Emperor of the universe"

def test_title_setter_none():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.title = None

def test_title_setter_int():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.title = 1234

def test_title_setter_length_zero():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.title = ""

def test_title_setter_spaces():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.title = "       "

def test_title_setter_greater_than_50():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.title = "a" * 51

def test_title_setter_non_letters():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.title = "3mp3r0r 0f th3 Un1v3r$3"

# ------ Testing loc setter ------
def test_loc_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.loc = "Andromeda Galaxy"
    assert cred.loc == "Andromeda Galaxy"

def test_loc_setter_none():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.loc = None

def test_loc_setter_int():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.loc = 1234

def test_loc_setter_length_zero():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.loc = ""

def test_loc_setter_spaces():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.loc = "       "
    
def test_loc_setter_greater_than_75():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.loc = "a" *76

def test_loc_setter_non_letters():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.loc = "4ndr0m3d4 G414xy"

# ----- Test Credentials Json Methods -----
class TestCredentialsJsonMethods:

    def test_from_json_object_valid_manager(self):
        content = {
            "id": 1,
            "fName": "Alice",
            "lName": "Smith",
            "dept": "Engineering",
            "title": "Manager",
            "loc": "HQ"
        }
        cred = Credentials.from_json_object(content)
        assert isinstance(cred, Credentials)
        assert cred.title == "Manager"  # stays Manager
        assert cred.fName == "Alice"
        assert cred.lName == "Smith"
        assert cred.dept == "Engineering"
        assert cred.loc == "HQ"

    def test_from_json_object_valid_non_manager(self):
        content = {
            "id": 2,
            "fName": "Bob",
            "lName": "Jones",
            "dept": "Sales",
            "title": "Intern",  # should be converted
            "loc": "Remote"
        }
        cred = Credentials.from_json_object(content)
        assert cred.title == "Employee"  # converted
        assert cred.dept == "Sales"

    @pytest.mark.parametrize("invalid_content", [
        "not a dict",  # Not a dictionary
        {"mesg": "Authentication failed"},  # Contains error_field
        {"id": 1, "fName": "Alice"}  # Missing required fields
    ])
    def test_from_json_object_invalid(self, invalid_content):
        with pytest.raises(ValueError):
            Credentials.from_json_object(invalid_content)

# ------ Testing Token setter ------
def test_token_setter_valid():
    tok = Token("1" * 250)
    assert tok.token == "1" * 250

def test_token_setter_none():
    with pytest.raises(ValueError, match="Token can not be None"):
        Token(None)

def test_token_setter_int():
    with pytest.raises(ValueError, match="Token must be string"):
        Token(1234)

def test_token_setter_length_zero():
    with pytest.raises(ValueError, match="No token provided"):
        Token("")

def test_token_setter_less_than_250():
    with pytest.raises(ValueError, match="Token is too short"):
        Token("1" * 200)

def test_token_setter_greater_than_400():
    with pytest.raises(ValueError, match="Token is too long"):
        Token("1" * 401)


class TestTokenJsonMethods:

    # --- Tests for from_json_object ---
    def test_from_json_object_valid(self):
        content = {"token": "A" * 300}  # valid token length
        token_obj = Token.from_json_object(content)
        assert isinstance(token_obj, Token)
        assert token_obj.token == "A" * 300

    @pytest.mark.parametrize("invalid_content", [
        "not a dict",  # Not a dictionary
        {},  # Missing token field
        {"key": "value"}  # Wrong key
    ])
    def test_from_json_object_invalid(self, invalid_content):
        with pytest.raises(ValueError):
            Token.from_json_object(invalid_content)

    # --- Tests for to_json_object ---
    def test_to_json_object_returns_correct_dict(self):
        token_obj = Token("B" * 300)
        result = token_obj.to_json_object()
        assert isinstance(result, dict)
        assert result == {"token": "B" * 300}

    # --- Round-trip test ---
    def test_round_trip_json_methods(self):
        original_dict = {"token": "C" * 300}
        token_obj = Token.from_json_object(original_dict)
        new_dict = token_obj.to_json_object()
        assert new_dict == original_dict