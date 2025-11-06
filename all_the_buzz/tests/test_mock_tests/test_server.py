import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from all_the_buzz.server import authentication_middleware, create_a_new_joke, retrieve_public_jokes_collection, Credentials, ResponseCode
from all_the_buzz.entities.record_entities import Joke

# Mock Credentials
manager_creds = Credentials(id=1, fName="Alice", lName="Smith", dept="Eng", title="Manager", loc="USA")
employee_creds = Credentials(id=2, fName="Bob", lName="Jones", dept="Eng", title="Employee", loc="USA")

app = Flask(__name__)
app.add_url_rule("/jokes", view_func=retrieve_public_jokes_collection)
app.add_url_rule("/jokes", view_func=create_a_new_joke, methods=["POST"])

# TEST THE ROUTE
@app.route("/test")
@authentication_middleware
def test_route(**kwargs):
    credentials = kwargs.get("credentials")
    return jsonify({"message": "success", "user": credentials.fName})

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_missing_token(client):
    response = client.get("/test")
    assert response.status_code == 401  # MissingToken maps to 401

@patch("all_the_buzz.server.authentication")
def test_invalid_token(mock_auth, client):
    mock_auth.return_value = ResponseCode("InvalidToken")
    response = client.get("/test", headers={"Bearer": "fake"})
    assert response.status_code == 401

@patch("all_the_buzz.server.authentication")
def test_valid_credentials(mock_auth, client):
    mock_auth.return_value = Credentials(
        id=123,
        fName="Test",
        lName="User",
        dept="Engineering",
        title="Manager",
        loc="USA"
    )
    response = client.get("/test", headers={"Bearer": "valid"})
    assert response.status_code == 200
    assert response.json["user"] == "Test"


# ------------------------------- retrieve_public_jokes_collection -------------------------------


# --- Authorized user, no filter ---
@patch("all_the_buzz.server.authentication")
@patch("all_the_buzz.server.get_dao_set_credentials")
def test_get_all_jokes(mock_dao_factory, mock_auth, client):
    mock_auth.return_value = Credentials(id=1, fName="Test", lName="User", dept="Eng", title="Manager", loc="USA")
    mock_dao = MagicMock()
    mock_dao.get_all_records.return_value = [{"joke": "funny"}]
    mock_dao_factory.return_value = mock_dao

    response = client.get("/jokes", headers={"Bearer": "valid"})
    assert response.status_code == 200
    assert "funny" in response.data.decode()
    mock_dao.get_all_records.assert_called_once()
    mock_dao.clear_credentials.assert_called_once()

# --- Authorized user, valid filter ---
@patch("all_the_buzz.server.authentication")
@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.convert_filter_types")
def test_get_filtered_jokes(mock_convert, mock_dao_factory, mock_auth, client):
    mock_auth.return_value = Credentials(id=1, fName="Test", lName="User", dept="Eng", title="Employee", loc="USA")
    mock_convert.return_value = {"difficulty": 2}
    mock_dao = MagicMock()
    mock_dao.get_by_fields.return_value = [{"joke": "filtered"}]
    mock_dao_factory.return_value = mock_dao

    response = client.get("/jokes?difficulty=2", headers={"Bearer": "valid"})
    assert response.status_code == 200
    assert "filtered" in response.data.decode()
    mock_dao.get_by_fields.assert_called_once_with({"difficulty": 2})

# --- Authorized user, invalid filter ---
@patch("all_the_buzz.server.authentication")
@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.convert_filter_types")
def test_invalid_filter(mock_convert, mock_dao_factory, mock_auth, client):
    mock_auth.return_value = Credentials(id=1, fName="Test", lName="User", dept="Eng", title="Manager", loc="USA")
    mock_convert.return_value = None
    mock_dao = MagicMock()
    mock_dao_factory.return_value = mock_dao

    response = client.get("/jokes?difficulty=abc", headers={"Bearer": "valid"})
    assert response.status_code == 400  # Assuming InvalidFilter maps to 400
    mock_dao.clear_credentials.assert_called_once()

# --- Unauthorized user ---
@patch("all_the_buzz.server.authentication")
def test_unauthorized_user(mock_auth, client):
    mock_auth.return_value = Credentials(id=1, fName="Test", lName="User", dept="Eng", title="Intern", loc="USA")
    response = client.get("/jokes", headers={"Bearer": "valid"})
    assert response.status_code == 401


# ------------------------------- create_a_new_joke as employee -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.Joke.from_json_object")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_creates_joke_success(mock_auth, mock_joke, mock_dao, client):
    mock_joke.return_value = Joke()
    mock_dao_instance = MagicMock()
    mock_dao_instance.create_record.return_value = ResponseCode("PendingSuccess")
    mock_dao.return_value = mock_dao_instance

    response = client.post("/jokes", json={
        "level": 1,
        "content": {"type": "one_liner", "text": "Funny joke"},
        "language": "english"
    })
    assert response.status_code == 202
    mock_dao_instance.create_record.assert_called_once()

# ------------------------------- retrieve private jokes collection -------------------------------