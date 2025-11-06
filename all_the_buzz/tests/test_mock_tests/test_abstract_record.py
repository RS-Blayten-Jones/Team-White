import pytest
from bson import ObjectId
from unittest.mock import MagicMock
from all_the_buzz.database_operations.abstract_record import DatabaseAccessObject
from all_the_buzz.entities.credentials_entity import Credentials
from all_the_buzz.utilities.error_handler import ResponseCode

# Concrete subclass for testing
class DAOStub(DatabaseAccessObject):
    __test__ = False  # Prevent pytest from collecting this as a test class
    pass

# ---------------- Fixtures ---------------- #

@pytest.fixture
def mock_client():
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_client = MagicMock()
    mock_client.__getitem__.return_value = mock_db
    return mock_client

@pytest.fixture
def mock_collection():
    return MagicMock()

@pytest.fixture
def dao(mock_collection):
    mock_client = MagicMock()
    mock_client.__getitem__.return_value.__getitem__.return_value = mock_collection
    return DAOStub(table_name="test_table", client=mock_client, database_name="test_db")

# ---------------- Initialization & Credentials ---------------- #

def test_init_sets_collection(mock_client):
    dao = DAOStub(table_name="test_table", client=mock_client, database_name="test_db")
    assert dao._collection is not None
    assert isinstance(dao._collection, MagicMock)

def test_set_and_get_credentials():
    dao = DAOStub("table", MagicMock(), "db")
    creds = Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ")
    dao.set_credentials(creds)
    assert dao.get_credentials() == creds

def test_clear_credentials():
    dao = DAOStub("table", MagicMock(), "db")
    creds = Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ")
    dao.set_credentials(creds)
    dao.clear_credentials()
    assert dao.get_credentials() is None

# ---------------- RBAC Tests ---------------- #

def test_rbac_action_allows_manager():
    dao = DAOStub("table", MagicMock(), "db")
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))

    @DatabaseAccessObject.rbac_action("read")
    def sample_method(self):
        return "allowed"

    assert sample_method(dao) == "allowed"

def test_rbac_action_denies_employee():
    dao = DAOStub("table", MagicMock(), "db")
    dao.set_credentials(Credentials(id=1, fName="Bob", lName="Jones", dept="IT", title="Intern", loc="HQ"))

    @DatabaseAccessObject.rbac_action("read")
    def sample_method(self):
        return "allowed"

    result = sample_method(dao)
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "PermissionIncongruency"

def test_rbac_action_no_credentials():
    dao = DAOStub("table", MagicMock(), "db")

    @DatabaseAccessObject.rbac_action("read")
    def sample_method(self):
        return "allowed"

    result = sample_method(dao)
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "PermissionIncongruency"

# ---------------- DAO Method Tests ---------------- #

from bson import ObjectId
from all_the_buzz.entities.credentials_entity import Credentials
from all_the_buzz.utilities.error_handler import ResponseCode

def test_get_short_record(dao, mock_collection):
    # Add Manager credentials
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))

    mock_collection.aggregate.return_value = [{"_id": "1"*24, "content": "short text"}]
    result = dao.get_short_record(numReturned=1, filter={"type": "test"}, max_length=80)

    assert isinstance(result, list)
    assert result[0]["content"] == "short text"
    mock_collection.aggregate.assert_called_once()


def test_get_short_record_fewer_results(dao, mock_collection):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    mock_collection.aggregate.return_value = [{"_id": "123", "content": "short text"}]
    result = dao.get_short_record(numReturned=3)
    assert len(result) == 1


def test_update_record_success(dao, mock_collection):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    mock_collection.update_one.return_value.matched_count = 1
    result = dao.update_record(ID=str(ObjectId()), updates={"field": "value"})
    assert isinstance(result, ResponseCode)
    assert result.get_data() == str(ObjectId()) or isinstance(result.get_data(), str)
    mock_collection.update_one.assert_called_once()


def test_update_record_not_found(dao, mock_collection):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    mock_collection.update_one.return_value.matched_count = 0
    result = dao.update_record(ID=str(ObjectId()), updates={"field": "value"})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "ResourceNotFound"


def test_update_record_empty_updates(dao):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    result = dao.update_record(ID=str(ObjectId()), updates={})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "MalformedContent"


def test_create_record(dao, mock_collection):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    mock_collection.insert_one.return_value.inserted_id = ObjectId()
    result = dao.create_record({"field": "value"})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "PostSuccess"


def test_delete_record_success(dao, mock_collection):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    mock_collection.delete_one.return_value.deleted_count = 1
    result = dao.delete_record(ID=str(ObjectId()))
    assert result.get_data()["deleted_count"] == 1


def test_delete_record_not_found(dao, mock_collection):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    mock_collection.delete_one.return_value.deleted_count = 0
    result = dao.delete_record(ID=str(ObjectId()))
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "ResourceNotFound"


def test_delete_record_by_field_success(dao, mock_collection):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    mock_collection.delete_many.return_value.deleted_count = 2
    result = dao.delete_record_by_field({"field": "value"})
    assert result.get_data()["deleted_count"] == 2


def test_delete_record_by_field_empty_filter(dao):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    result = dao.delete_record_by_field({})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "MalformedContent"


def test_delete_record_by_field_multiple_fields(dao):
    dao.set_credentials(Credentials(id=1, fName="Alice", lName="Smith", dept="IT", title="Manager", loc="HQ"))
    result = dao.delete_record_by_field({"field1": "value1", "field2": "value2"})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "MalformedContent"

# ---- Tests for non-managers -----
@pytest.mark.parametrize("action,method,args", [
    ("read", "get_short_record", {"numReturned": 1}),
    ("update", "update_record", {"ID": "123456789012345678901234", "updates": {"field": "value"}}),
    ("create", "create_record", {"entry": {"field": "value"}}),
    ("delete", "delete_record", {"ID": "123456789012345678901234"}),
    ("delete", "delete_record_by_field", {"filter": {"field": "value"}}),
])
def test_rbac_denies_employee(dao, action, method, args):
    # Set Intern credentials (non-manager)
    dao.set_credentials(Credentials(id=2, fName="Bob", lName="Jones", dept="IT", title="Intern", loc="HQ"))

    # Call the method dynamically
    func = getattr(dao, method)
    result = func(**args)

    # Assert RBAC denial
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "PermissionIncongruency"