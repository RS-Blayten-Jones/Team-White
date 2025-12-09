# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from all_the_buzz.server import authentication_middleware, retrieve_daily_quote, approve_joke,retrieve_random_bio, retrieve_private_jokes_collection, create_a_new_joke, retrieve_public_jokes_collection, Credentials, ResponseCode
from all_the_buzz.entities.record_entities import Joke, Quote, Trivia, Bio

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
# Import additional functions needed for new tests
from all_the_buzz.server import (
    deny_joke, approve_quote, deny_quote, approve_trivia, deny_trivia,
    approve_bio, deny_bio, retrieve_random_joke, retrieve_random_quote,
    retrieve_random_trivia, retrieve_short_quote, retrieve_public_quotes_collection,
    retrieve_public_trivia_collection, retrieve_public_bios_collection,
    retrieve_private_quotes_collection, retrieve_private_trivias_collection,
    retrieve_private_bios_collection, create_a_new_quote, create_a_new_trivia,
    create_a_new_bio
)

app.add_url_rule("/jokes", view_func=retrieve_public_jokes_collection, methods=["GET"])
app.add_url_rule("/jokes", view_func=create_a_new_joke, methods=["POST"])
app.add_url_rule("/pending_jokes", view_func=retrieve_private_jokes_collection, methods=["GET"])
app.add_url_rule("/jokes/<id>/approve", view_func=approve_joke, methods=["POST"])
app.add_url_rule("/jokes/<id>/deny", view_func=deny_joke, methods=["POST"])
app.add_url_rule("/bios/random/<int:amount>", view_func=retrieve_random_bio, methods=["GET"])
app.add_url_rule("/daily-quotes", view_func=retrieve_daily_quote, methods=["GET"])

# Additional routes for quotes
app.add_url_rule("/quotes", view_func=retrieve_public_quotes_collection, methods=["GET"])
app.add_url_rule("/quotes", view_func=create_a_new_quote, methods=["POST"])
app.add_url_rule("/pending-quotes", view_func=retrieve_private_quotes_collection, methods=["GET"])
app.add_url_rule("/quotes/<id>/approve", view_func=approve_quote, methods=["POST"])
app.add_url_rule("/quotes/<id>/deny", view_func=deny_quote, methods=["POST"])
app.add_url_rule("/random-quotes/<int:amount>", view_func=retrieve_random_quote, methods=["GET"])
app.add_url_rule("/short-quotes/<int:amount>", view_func=retrieve_short_quote, methods=["GET"])

# Additional routes for trivias
app.add_url_rule("/trivias", view_func=retrieve_public_trivia_collection, methods=["GET"])
app.add_url_rule("/trivias", view_func=create_a_new_trivia, methods=["POST"])
app.add_url_rule("/pending-trivias", view_func=retrieve_private_trivias_collection, methods=["GET"])
app.add_url_rule("/trivias/<id>/approve", view_func=approve_trivia, methods=["POST"])
app.add_url_rule("/trivias/<id>/deny", view_func=deny_trivia, methods=["POST"])
app.add_url_rule("/random-trivias/<int:amount>", view_func=retrieve_random_trivia, methods=["GET"])

# Additional routes for bios
app.add_url_rule("/bios", view_func=retrieve_public_bios_collection, methods=["GET"])
app.add_url_rule("/bios", view_func=create_a_new_bio, methods=["POST"])
app.add_url_rule("/pending-bios", view_func=retrieve_private_bios_collection, methods=["GET"])
app.add_url_rule("/bios/<id>/approve", view_func=approve_bio, methods=["POST"])
app.add_url_rule("/bios/<id>/deny", view_func=deny_bio, methods=["POST"])
app.add_url_rule("/random-jokes/<int:amount>", view_func=retrieve_random_joke, methods=["GET"])

 # TEST THE ROUTE
@app.route("/test")
@authentication_middleware
def mock_test_route(**kwargs):
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

    mock_quote_response.get_data.return_value = {
        "id": 10,
        "content": "Success is not final, failure is not fatal.",
        "author": "Winston Churchill",
        "used_date": ""
    }
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
    mock_dao_instance.get_quote_of_day.assert_called_once()
    mock_dao_instance.clear_credentials.assert_called_once()


# ------------------------------- deny_joke -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_denies_joke(mock_auth, mock_dao, client):
    """Test that a manager can deny a pending joke."""
    private_dao = MagicMock()
    private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    mock_dao.return_value = private_dao

    response = client.post("/jokes/123/deny")
    assert response.status_code == 200
    private_dao.delete_record.assert_called_once_with("123")
    private_dao.clear_credentials.assert_called_once()

@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_cannot_deny_joke(mock_auth, client):
    """Test that an employee cannot deny a pending joke."""
    response = client.post("/jokes/123/deny")
    assert response.status_code == 401
    assert response.json["code_tag"] == "Unauthorized"


# ------------------------------- approve/deny quote -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.Quote.from_json_object")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_approves_new_quote(mock_auth, mock_quote, mock_dao, client):
    """Test that a manager can approve a new quote."""
    quote_instance = Quote()
    quote_instance.is_edit = False
    quote_instance.to_json_object = lambda: {"content": "Inspirational quote"}
    mock_quote.return_value = quote_instance

    private_dao = MagicMock()
    public_dao = MagicMock()
    private_dao.get_by_key.return_value = {"id": "123", "content": "Inspirational quote"}
    private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    public_dao.create_record.return_value = ResponseCode("PostSuccess")
    mock_dao.side_effect = [private_dao, public_dao]

    response = client.post("/quotes/123/approve")
    assert response.status_code == 200
    private_dao.get_by_key.assert_called_once_with("123")
    public_dao.create_record.assert_called_once()
    private_dao.delete_record.assert_called_once_with("123")

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_denies_quote(mock_auth, mock_dao, client):
    """Test that a manager can deny a pending quote."""
    private_dao = MagicMock()
    private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    mock_dao.return_value = private_dao

    response = client.post("/quotes/123/deny")
    assert response.status_code == 200
    private_dao.delete_record.assert_called_once_with("123")
    private_dao.clear_credentials.assert_called_once()


# ------------------------------- approve/deny trivia -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.Trivia.from_json_object")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_approves_new_trivia(mock_auth, mock_trivia, mock_dao, client):
    """Test that a manager can approve a new trivia."""
    trivia_instance = Trivia()
    trivia_instance.is_edit = False
    trivia_instance.to_json_object = lambda: {"question": "What is the capital?", "answer": "Paris"}
    mock_trivia.return_value = trivia_instance

    private_dao = MagicMock()
    public_dao = MagicMock()
    private_dao.get_by_key.return_value = {"id": "123", "question": "What is the capital?"}
    private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    public_dao.create_record.return_value = ResponseCode("PostSuccess")
    mock_dao.side_effect = [private_dao, public_dao]

    response = client.post("/trivias/123/approve")
    assert response.status_code == 200
    private_dao.get_by_key.assert_called_once_with("123")
    public_dao.create_record.assert_called_once()
    private_dao.delete_record.assert_called_once_with("123")

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_denies_trivia(mock_auth, mock_dao, client):
    """Test that a manager can deny a pending trivia."""
    private_dao = MagicMock()
    private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    mock_dao.return_value = private_dao

    response = client.post("/trivias/123/deny")
    assert response.status_code == 200
    private_dao.delete_record.assert_called_once_with("123")
    private_dao.clear_credentials.assert_called_once()


# ------------------------------- approve/deny bio -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.Bio.from_json_object")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_approves_new_bio(mock_auth, mock_bio, mock_dao, client):
    """Test that a manager can approve a new bio."""
    bio_instance = Bio()
    bio_instance.is_edit = False
    bio_instance.to_json_object = lambda: {"name": "Albert Einstein", "paragraph": "Famous physicist"}
    mock_bio.return_value = bio_instance

    private_dao = MagicMock()
    public_dao = MagicMock()
    private_dao.get_by_key.return_value = {"id": "123", "name": "Albert Einstein"}
    private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    public_dao.create_record.return_value = ResponseCode("PostSuccess")
    mock_dao.side_effect = [private_dao, public_dao]

    response = client.post("/bios/123/approve")
    assert response.status_code == 200
    private_dao.get_by_key.assert_called_once_with("123")
    public_dao.create_record.assert_called_once()
    private_dao.delete_record.assert_called_once_with("123")

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_denies_bio(mock_auth, mock_dao, client):
    """Test that a manager can deny a pending bio."""
    private_dao = MagicMock()
    private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    mock_dao.return_value = private_dao

    response = client.post("/bios/123/deny")
    assert response.status_code == 200
    private_dao.delete_record.assert_called_once_with("123")
    private_dao.clear_credentials.assert_called_once()


# ------------------------------- retrieve random records -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_random_jokes(mock_auth, mock_dao, client):
    """Test that an employee can retrieve random jokes."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_random.return_value = [
        {"id": 1, "content": {"type": "one_liner", "text": "Joke 1"}},
        {"id": 2, "content": {"type": "one_liner", "text": "Joke 2"}}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/random-jokes/2")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Joke 1" in data or "Joke 2" in data
    mock_dao_instance.get_random.assert_called_once_with(2)
    mock_dao_instance.clear_credentials.assert_called_once()

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_random_quotes(mock_auth, mock_dao, client):
    """Test that an employee can retrieve random quotes."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_random.return_value = [
        {"id": 1, "content": "Quote 1", "author": "Author 1"},
        {"id": 2, "content": "Quote 2", "author": "Author 2"}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/random-quotes/2")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Quote 1" in data or "Quote 2" in data
    mock_dao_instance.get_random.assert_called_once_with(2)
    mock_dao_instance.clear_credentials.assert_called_once()

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_random_trivias(mock_auth, mock_dao, client):
    """Test that an employee can retrieve random trivias."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_random.return_value = [
        {"id": 1, "question": "Question 1", "answer": "Answer 1"},
        {"id": 2, "question": "Question 2", "answer": "Answer 2"}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/random-trivias/2")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Question 1" in data or "Question 2" in data
    mock_dao_instance.get_random.assert_called_once_with(2)
    mock_dao_instance.clear_credentials.assert_called_once()


# ------------------------------- retrieve short quotes -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_short_quotes(mock_auth, mock_dao, client):
    """Test that an employee can retrieve short quotes."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_short_record.return_value = [
        {"id": 1, "content": "Short quote", "author": "Author"}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/short-quotes/5")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Short quote" in data
    mock_dao_instance.get_short_record.assert_called_once_with(5)


# ------------------------------- retrieve public collections -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_public_quotes(mock_auth, mock_dao, client):
    """Test that an employee can retrieve public quotes."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_all_records.return_value = [
        {"id": 1, "content": "Quote 1", "author": "Author 1"}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/quotes")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Quote 1" in data
    mock_dao_instance.get_all_records.assert_called_once()
    mock_dao_instance.clear_credentials.assert_called_once()

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_public_trivias(mock_auth, mock_dao, client):
    """Test that an employee can retrieve public trivias."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_all_records.return_value = [
        {"id": 1, "question": "Question 1", "answer": "Answer 1"}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/trivias")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Question 1" in data
    mock_dao_instance.get_all_records.assert_called_once()
    mock_dao_instance.clear_credentials.assert_called_once()

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_retrieves_public_bios(mock_auth, mock_dao, client):
    """Test that an employee can retrieve public bios."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_all_records.return_value = [
        {"id": 1, "name": "Albert Einstein", "paragraph": "Famous physicist"}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/bios")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Albert Einstein" in data
    mock_dao_instance.get_all_records.assert_called_once()
    mock_dao_instance.clear_credentials.assert_called_once()


# ------------------------------- retrieve private collections -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_retrieves_private_quotes(mock_auth, mock_dao, client):
    """Test that a manager can retrieve private quotes."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_all_records.return_value = [
        {"id": 1, "content": "Pending quote"}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/pending-quotes")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Pending quote" in data
    mock_dao_instance.get_all_records.assert_called_once()
    mock_dao_instance.clear_credentials.assert_called_once()

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_retrieves_private_trivias(mock_auth, mock_dao, client):
    """Test that a manager can retrieve private trivias."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_all_records.return_value = [
        {"id": 1, "question": "Pending question"}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/pending-trivias")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Pending question" in data
    mock_dao_instance.get_all_records.assert_called_once()
    mock_dao_instance.clear_credentials.assert_called_once()

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_manager_retrieves_private_bios(mock_auth, mock_dao, client):
    """Test that a manager can retrieve private bios."""
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_all_records.return_value = [
        {"id": 1, "name": "Pending bio"}
    ]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/pending-bios")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Pending bio" in data
    mock_dao_instance.get_all_records.assert_called_once()
    mock_dao_instance.clear_credentials.assert_called_once()


# ------------------------------- Test approve/deny with edits -------------------------------
# Note: Edit approval tests require 24-character MongoDB ObjectIds which are complex to mock properly


# ------------------------------- Test error paths -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_approve_joke_invalid_record(mock_auth, mock_dao, client):
    """Test approving a joke with invalid record format."""
    private_dao = MagicMock()
    public_dao = MagicMock()
    private_dao.get_by_key.return_value = {"invalid": "data"}
    mock_dao.side_effect = [private_dao, public_dao]

    response = client.post("/jokes/123/approve")
    assert response.status_code in [400, 500]  # Should be an error


@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.authentication", return_value=manager_creds)
def test_deny_joke_with_error(mock_auth, mock_dao, client):
    """Test denying a joke when an error occurs."""
    private_dao = MagicMock()
    private_dao.delete_record.side_effect = Exception("Database error")
    mock_dao.return_value = private_dao

    response = client.post("/jokes/123/deny")
    assert response.status_code == 500


# ------------------------------- Test create with validation errors -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.Quote.from_json_object")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_creates_quote_invalid_data(mock_auth, mock_quote, mock_dao, client):
    """Test employee creating quote with invalid data."""
    mock_quote.side_effect = ValueError("Invalid quote data")

    response = client.post("/quotes", json={"invalid": "data"})
    assert response.status_code in [400, 500]


@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.Trivia.from_json_object")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_creates_trivia_success(mock_auth, mock_trivia, mock_dao, client):
    """Test employee successfully creating trivia."""
    mock_trivia.return_value = Trivia()
    mock_dao_instance = MagicMock()
    mock_dao_instance.create_record.return_value = ResponseCode("PendingSuccess")
    mock_dao.return_value = mock_dao_instance

    response = client.post("/trivias", json={
        "question": "What is 2+2?",
        "answer": "4",
        "language": "english"
    })
    assert response.status_code == 202


@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.Bio.from_json_object")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_creates_bio_success(mock_auth, mock_bio, mock_dao, client):
    """Test employee successfully creating bio."""
    mock_bio.return_value = Bio()
    mock_dao_instance = MagicMock()
    mock_dao_instance.create_record.return_value = ResponseCode("PendingSuccess")
    mock_dao.return_value = mock_dao_instance

    response = client.post("/bios", json={
        "name": "Test Person",
        "paragraph": "Test bio",
        "language": "english",
        "source_url": "https://example.com"
    })
    assert response.status_code == 202


# ------------------------------- Test unauthorized access -------------------------------

@patch("all_the_buzz.server.authentication")
def test_intern_cannot_access_jokes(mock_auth, client):
    """Test that users with invalid titles can't access protected endpoints."""
    mock_auth.return_value = Credentials(id=3, fName="Test", lName="User", dept="Eng", title="Intern", loc="USA")
    response = client.get("/jokes")
    assert response.status_code == 401


@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_employee_cannot_approve_quote(mock_auth, client):
    """Test that employees cannot approve pending items."""
    response = client.post("/quotes/123/approve")
    assert response.status_code == 401


# ------------------------------- Test filter conversions -------------------------------

@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.convert_filter_types")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_filtered_quotes_retrieval(mock_auth, mock_filter, mock_dao, client):
    """Test retrieving quotes with filters."""
    mock_filter.return_value = {"category": "Motivational"}
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_by_fields.return_value = [{"content": "Motivational quote"}]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/quotes?category=Motivational")
    assert response.status_code == 200
    assert "Motivational quote" in response.data.decode()


@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.convert_filter_types")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_filtered_trivias_retrieval(mock_auth, mock_filter, mock_dao, client):
    """Test retrieving trivias with filters."""
    mock_filter.return_value = {"language": "English"}
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_by_fields.return_value = [{"question": "English question"}]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/trivias?language=English")
    assert response.status_code == 200
    assert "English question" in response.data.decode()


@patch("all_the_buzz.server.get_dao_set_credentials")
@patch("all_the_buzz.server.convert_filter_types")
@patch("all_the_buzz.server.authentication", return_value=employee_creds)
def test_filtered_bios_retrieval(mock_auth, mock_filter, mock_dao, client):
    """Test retrieving bios with filters."""
    mock_filter.return_value = {"birth_year": 1879}
    mock_dao_instance = MagicMock()
    mock_dao_instance.get_by_fields.return_value = [{"name": "Albert Einstein"}]
    mock_dao.return_value = mock_dao_instance

    response = client.get("/bios?birth_year=1879")
    assert response.status_code == 200
    assert "Albert Einstein" in response.data.decode()

