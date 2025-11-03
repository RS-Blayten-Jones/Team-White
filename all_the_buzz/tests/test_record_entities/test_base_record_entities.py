import pytest
from entities import BaseRecord

# Dummy subclass to test BaseRecord
class DummyRecord(BaseRecord):
    def to_json_object(self):
        return {}

    @staticmethod
    def from_json_object(content):
        return DummyRecord()

# --- Tests ---

def test_valid_base_record_initialization():
    record = DummyRecord(id=1, ref_id=2, is_edit=False, language="english")
    assert record.id == 1
    assert record.ref_id == 2
    assert record.is_edit is False
    assert record.language == "english"

def test_is_edit_requires_ref_id():
    with pytest.raises(ValueError, match="Reference ID is required for edits"):
        DummyRecord(id=1, ref_id=None, is_edit=True)

def test_language_none_raises():
    with pytest.raises(ValueError, match="Language can not be none"):
        DummyRecord(language=None)

def test_language_not_string_raises():
    with pytest.raises(ValueError, match="Language must be a string"):
        DummyRecord(language=123)

def test_setters_work_as_expected():
    record = DummyRecord()
    record.id = 10
    record.ref_id = 20
    record.language = "french"
    record.is_edit = False

    assert record.id == 10
    assert record.ref_id == 20
    assert record.language == "french"
    assert record.is_edit is False