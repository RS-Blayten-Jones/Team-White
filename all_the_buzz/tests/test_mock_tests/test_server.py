import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from all_the_buzz.server import authentication_middleware, retrieve_daily_quote, approve_joke,retrieve_random_bio, retrieve_private_jokes_collection, create_a_new_joke, retrieve_public_jokes_collection, Credentials, ResponseCode
from all_the_buzz.entities.record_entities import Joke

"""
This file runs tests over the essential functionalities of the project, as specifically stated in the TeamWhite.pdf file

    -Create new records (create new joke record is the example tested)
    -Approve new records as Manager (approve new joke record is the example tested)
    -Request a joke by difficulty
    -Request a random entry (retrieve random bio is the example tested)
    -Implement funcitionality to have a daily quote that has not been used within the year (retrieve_daily_quote)
"""

# ----------------
# Mock Credentials
# ----------------
manager_creds = Credentials(id=1, fName="Alice", lName="Smith", dept="Eng", title="Manager", loc="USA")
employee_creds = Credentials(id=2, fName="Bob", lName="Jones", dept="Eng", title="Employee", loc="USA")

app = Flask(__name__)
app.add_url_rule("/jokes", view_func=retrieve_public_jokes_collection, methods=["GET"])
app.add_url_rule("/jokes", view_func=create_a_new_joke, methods=["POST"])
app.add_url_rule("/pending_jokes", view_func=retrieve_private_jokes_collection, methods=["GET"])
app.add_url_rule("/jokes/<id>/approve", view_func=approve_joke, methods=["POST"])
app.add_url_rule("/bios/random/<int:amount>", view_func=retrieve_random_bio, methods=["GET"])
app.add_url_rule("/daily-quotes", view_func=retrieve_daily_quote, methods=["GET"])

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
    # with app.app_context():
    response = client.get("/test")  # No Bearer header
    assert response.status_code == 401
    assert response.json["code_tag"] == "InvalidToken"

@patch("all_the_buzz.server.authentication")
def test_invalid_token(mock_auth, client):
    mock_auth.return_value = ResponseCode("InvalidToken")
    response = client.get("/test", headers={"Bearer": "fake"})  # ✅ Use Bearer key
    assert response.status_code == 401
    assert response.json["code_tag"] == "InvalidToken"

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
    response = client.get("/test", headers={"Bearer": "valid"})  # ✅ Use Bearer key
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

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_retrieves_private_jokes(mock_auth, mock_dao, client):
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_all_records.return_value = [{"id": 1, "content": "Funny joke"}]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/pending_jokes")
    assert response.status_code == 200
    assert "Funny joke" in response.data.decode()  # JSON string returned
    mock_dao_instance.get_all_records.assert_called_once()
    mock_dao_instance.clear_credentials.assert_called_once()

@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_unauthorized_access(mock_auth, client):
    response = client.get("/pending_jokes")
    assert response.status_code == 401
    assert response.json["code_tag"] == "Unauthorized"


# ------------------------------- approve joke -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.Joke.from_json_object")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_approves_new_joke(mock_auth, mock_joke, mock_dao, client):
    # Mock Joke with is_edit=False
    joke_instance = Joke()
    joke_instance.is_edit = False
    joke_instance.to_json_object = lambda: {"content": "Funny joke"}
    mock_joke.return_value = joke_instance

    # Mock DAOs
    private_dao = MagicMock()
    public_dao = MagicMock()
    private_dao.get_by_key.return_value = {"id": "123", "content": "Funny joke"}
    private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    public_dao.create_record.return_value = ResponseCode("PostSuccess")
    mock_dao.side_effect = [private_dao, public_dao]

    response = client.post("/jokes/123/approve")
    assert response.status_code == 200
    private_dao.get_by_key.assert_called_once_with("123")
    public_dao.create_record.assert_called_once()
    private_dao.delete_record.assert_called_once_with("123")

@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_unauthorized(mock_auth, client):
    response = client.post("/jokes/123/approve")
    assert response.status_code == 401
    assert response.json["code_tag"] == "Unauthorized"

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_get_by_key_failure(mock_auth, mock_dao, client):
    private_dao = MagicMock()
    public_dao = MagicMock()
    private_dao.get_by_key.side_effect = Exception("RecordNotFound")
    mock_dao.side_effect = [private_dao, public_dao]

    response = client.post("/jokes/123/approve")
    assert response.status_code == 500
    assert "RecordNotFound" in response.json["code_tag"]


# ------------------------------- retrieve public joke by difficulty -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.convert_filter_types", return_value={"difficulty": 2})
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_jokes_by_difficulty(mock_auth, mock_filter, mock_dao, client):
    # Mock DAO behavior
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_by_fields.return_value = [
        {"id": 101, "content": "Tech joke", "difficulty": 2},
        {"id": 102, "content": "Another tech joke", "difficulty": 2}
    ]
    mock_dao.return_value = mock_dao_instance

    # Perform GET request with query param
    response = client.get("/jokes?difficulty=2")

    # Assertions
    assert response.status_code == 200
    data = response.data.decode()
    assert "Tech joke" in data
    assert "Another tech joke" in data
    mock_dao_instance.get_by_fields.assert_called_once_with({"difficulty": 2})
    mock_dao_instance.clear_credentials.assert_called_once()


# ------------------------------- retrieve random bio -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_random_bios(mock_auth, mock_dao, client):

    mock_dao_instance = MagicMock()
    mock_dao_instance.get_random.return_value = [
        {"id": 1, "bio": "Funny bio"},
        {"id": 2, "bio": "Another bio"}
    ]
    mock_dao.return_value = mock_dao_instance

    # Perform GET request with amount=2
    response = client.get("/bios/random/2")

    # Assertions
    assert response.status_code == 200
    data = response.data.decode()
    assert "Funny bio" in data
    assert "Another bio" in data
    mock_dao_instance.get_random.assert_called_once_with(2)
    mock_dao_instance.clear_credentials.assert_called_once()


# ------------------------------- retrieve daily quote -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_unused_quote(mock_auth, mock_dao, client):

    mock_dao_instance = MagicMock()
    mock_quote_response = MagicMock()

    mock_quote_response.get_data.return_value = [
        {"id": 10, "content": "Success is not final, failure is not fatal.", "author": "Winston Churchill", "used_date": ""},  # older than a year
        {"id": 11, "content": "Stay positive!", "author": "Alice", "used_date": "2025-03-01"},  # used this year
        {"id": 12, "content": "Keep learning!", "author": "Bob", "used_date": "2025-06-15"}     # used this year
    ]
    mock_dao_instance.get_quote_of_day.return_value = mock_quote_response
    mock_dao.return_value = mock_dao_instance

    # Perform GET request
    response = client.get("/daily-quotes")

    # Assertions
    assert response.status_code == 200
    data = response.data.decode()
    # Return the quote that hasn't been used within the year
    assert "Success is not final" in data
    assert "Winston Churchill" in data
    assert "Stay positive!" in data or "Keep learning!" in data
    mock_dao_instance.get_quote_of_day.assert_called_once()
    mock_dao_instance.clear_credentials.assert_called_once()



