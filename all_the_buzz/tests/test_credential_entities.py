"""
This file runs unit tests on setter methods for credentials entities

To unit test:
(.venv)...\all_the_buzz> pip install pytest
(.venv)...\all_the_buzz> python -m pytest

To test coverage:
(.venv)...\all_the_buzz> pip install pytest-cov
(.venv)...\all_the_buzz> python -m pytest --cov=entities --cov-report=term
(.venv)...\all_the_buzz> python -m pytest --cov=entities --cov-report=term-missing
"""

from entities import Credentials, Token
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
    
# ------ Testing Fname setter ------
def test_fname_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.fname = "Mike"
    assert cred.fname == "Mike"
    
# Test for allowing apostrophes in names
# def test_fname_setter_valid_apostrophe():
#     cred = Credentials()
#     cred.id = 1234
#     cred.fname ="De'Wayne"
#     pass

def test_fname_setter_none():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.fname = None

def test_fname_setter_int():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.fname = 1234

def test_fname_setter_length_zero():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.fname = ""

def test_fname_setter_spaces():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.fname = "           "

def test_fname_setter_greater_than_50():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.fname = "a" * 51
    
# def test_fname_setter_non_letters():
#     cred = Credentials()
#     cred.id = 1234
#     with pytest.raises(ValueError):
#         cred.fname = "$p3nc3r"

# ------ Testing Lname setter ------
def test_lname_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.lname = "Jones"
    assert cred.lname == "Jones"

# Test for allowing apostrophes in names
# def test_lname_setter_valid_apostrophe():
#     cred = Credentials()
#     cred.id = 1234
#     cred.lname = "O'Conner"
#     assert cred.lname == "O'Conner"

def test_lname_setter_none():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lname = None

def test_lname_setter_int():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lname = 1234

def test_lname_setter_length_zero():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lname = ""

def test_lname_setter_spaces():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lname = "           "

def test_lname_setter_greater_than_50():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.lname = "a" * 51

# def test_lname_setter_non_letters():
#     cred = Credentials()
#     cred.id = 1234
#     with pytest.raises(ValueError):
#         cred.lname = "$p3nc3r"

# ------ Testing Department setter ------
def test_department_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.department = "Sales"
    assert cred.department == "Sales"

def test_department_setter_none():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.department = None

def test_department_setter_int():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.department = 1234

def test_department_setter_length_zero():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.department = ""

def test_department_setter_spaces():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.department = "       "

def test_department_setter_greater_than_35():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.department = "a" * 36

def test_department_setter_non_letters():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.department = "$4l3$"

# ------ Testing Title setter ------
def test_title_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.title = "Emperor of the Universe"
    assert cred.title == "Emperor of the Universe"

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

# ------ Testing Location setter ------
def test_location_setter_valid():
    cred = Credentials()
    cred.id = 1234
    cred.location = "Andromeda Galaxy"
    assert cred.location == "Andromeda Galaxy"

def test_location_setter_none():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.location = None

def test_location_setter_int():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.location = 1234

def test_location_setter_length_zero():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.location = ""

def test_location_setter_spaces():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.location = "       "
    
def test_location_setter_greater_than_75():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.location = "a" *76

def test_location_setter_non_letters():
    cred = Credentials()
    cred.id = 1234
    with pytest.raises(ValueError):
        cred.location = "4ndr0m3d4 G414xy"

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

