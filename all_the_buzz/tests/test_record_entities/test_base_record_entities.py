import pytest
from all_the_buzz.entities import BaseRecord

# Dummy subclass to test BaseRecord
class DummyRecord(BaseRecord):
    def to_json_object(self):
        return {}

    @staticmethod
    def from_json_object(content):
        return DummyRecord()

# ----- Test for valid BaseRecord initialization -----
def test_valid_base_record_initialization():
    id_hex_str = ("1" * 24)
    ref_id_hex_str = ("2" * 24)
    record = DummyRecord(id=id_hex_str, ref_id=ref_id_hex_str, is_edit=False, language="english")
    assert record.id == id_hex_str
    assert record.ref_id == ref_id_hex_str
    assert record.is_edit is False
    assert record.language == "english"

# ----- Test id setters -----
def test_invalid_base_record_id_type():
    id_hex_str = (1234)
    ref_id_hex_str = ("2" * 24)
    with pytest.raises(ValueError, match="Record ID must be either string or None"):
        DummyRecord(id=id_hex_str, ref_id=ref_id_hex_str, is_edit=False, language="english")

def test_invalid_base_record_id_length():
    id_hex_str = ("1" * 23)
    ref_id_hex_str = ("2" * 24)
    with pytest.raises(ValueError, match="Invalid Record ID"):
        DummyRecord(id=id_hex_str, ref_id=ref_id_hex_str, is_edit=False, language="english")
    
def test_invalid_base_record_id_hex_value():
    id_hex_str = ("$" * 24)
    ref_id_hex_str = ("2" * 24)
    with pytest.raises(ValueError, match="Invalid Record ID"):
        DummyRecord(id=id_hex_str, ref_id=ref_id_hex_str, is_edit=False, language="english")

# ----- Tests ref_id setters -----
def test_invalid_base_record_ref_id_type():
    id_hex_str = ("1" * 24)
    ref_id_hex_str = (1234)
    with pytest.raises(ValueError, match="Reference ID must be either string or None"):
        DummyRecord(id=id_hex_str, ref_id=ref_id_hex_str, is_edit=False, language="english")

def test_invalid_base_record_ref_id_length():
    id_hex_str = ("1" * 24)
    ref_id_hex_str = ("2" * 23)
    with pytest.raises(ValueError, match="Invalid Record ID"):
        DummyRecord(id=id_hex_str, ref_id=ref_id_hex_str, is_edit=False, language="english")
    
def test_invalid_base_record_ref_id_hex_value():
    id_hex_str = ("1" * 24)
    ref_id_hex_str = ("$" * 24)
    with pytest.raises(ValueError, match="Invalid Record ID"):
        DummyRecord(id=id_hex_str, ref_id=ref_id_hex_str, is_edit=False, language="english")

# ----- Tests is_edit setters -----
def test_is_edit_requires_ref_id():
    id_hex_str = ("1" * 24)
    with pytest.raises(ValueError, match="Reference ID is required for edits"):
        DummyRecord(id=id_hex_str, ref_id=None, is_edit=True, language="english")

# ----- Tests language setters -----
def test_invalid_language_None():
    id_hex_str = ("1" * 24)
    with pytest.raises(ValueError, match="Language can not be none"):
        DummyRecord(id= id_hex_str, ref_id=None, is_edit=False, language=None)

def test_invalid_language_type():
    id_hex_str = ("1" * 24)
    with pytest.raises(ValueError, match="Language must be a string"):
        DummyRecord(id= id_hex_str, ref_id=None, is_edit=False, language=123)

def test_setters_work_as_expected():
    record = DummyRecord()
    record.id = "1" * 24
    record.ref_id = None
    record.language = "french"
    record.is_edit = False

    assert record.id == "1" * 24
    assert record.ref_id == None
    assert record.language == "french"
    assert record.is_edit is False