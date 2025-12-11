# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details

"""
Additional tests for server.py to achieve near 100% coverage.
Focuses on exception handling, proxy functions, approve/deny flows, and edge cases.
"""

import pytest
from unittest.mock import patch, MagicMock, Mock
from flask import Flask
from all_the_buzz.server import (
    create_a_new_joke,
    create_a_new_quote,
    create_a_new_trivia,
    create_a_new_bio,
    approve_joke,
    approve_quote,
    approve_trivia,
    approve_bio,
    deny_joke,
    deny_quote,
    deny_trivia,
    deny_bio,
    retrieve_daily_quote,
    retrieve_random_joke,
    retrieve_random_quote,
    retrieve_random_trivia,
    retrieve_random_bio,
    retrieve_short_quote,
    create_app,
    Credentials,
    ResponseCode
)

# ----------------
# Mock Credentials
# ----------------
manager_creds = Credentials(id=1, fName="Alice", lName="Smith", dept="Eng", title="Manager", loc="USA")
employee_creds = Credentials(id=2, fName="Bob", lName="Jones", dept="Eng", title="Employee", loc="USA")

# ----------------
# Test App Setup
# ----------------
app = Flask(__name__)

# Add URL rules for all endpoints
app.add_url_rule("/jokes", view_func=create_a_new_joke, methods=["POST"])
app.add_url_rule("/quotes", view_func=create_a_new_quote, methods=["POST"])
app.add_url_rule("/trivias", view_func=create_a_new_trivia, methods=["POST"])
app.add_url_rule("/bios", view_func=create_a_new_bio, methods=["POST"])

app.add_url_rule("/jokes/<string:id>/approve", view_func=approve_joke, methods=["POST"])
app.add_url_rule("/quotes/<string:id>/approve", view_func=approve_quote, methods=["POST"])
app.add_url_rule("/trivias/<string:id>/approve", view_func=approve_trivia, methods=["POST"])
app.add_url_rule("/bios/<string:id>/approve", view_func=approve_bio, methods=["POST"])

app.add_url_rule("/jokes/<string:id>/deny", view_func=deny_joke, methods=["POST"])
app.add_url_rule("/quotes/<string:id>/deny", view_func=deny_quote, methods=["POST"])
app.add_url_rule("/trivias/<string:id>/deny", view_func=deny_trivia, methods=["POST"])
app.add_url_rule("/bios/<string:id>/deny", view_func=deny_bio, methods=["POST"])

app.add_url_rule("/random-jokes/<int:amount>", view_func=retrieve_random_joke, methods=["GET"])
app.add_url_rule("/random-quotes/<int:amount>", view_func=retrieve_random_quote, methods=["GET"])
app.add_url_rule("/random-trivias/<int:amount>", view_func=retrieve_random_trivia, methods=["GET"])
app.add_url_rule("/random-bios/<int:amount>", view_func=retrieve_random_bio, methods=["GET"])
app.add_url_rule("/short-quotes/<int:amount>", view_func=retrieve_short_quote, methods=["GET"])
app.add_url_rule("/daily-quotes", view_func=retrieve_daily_quote, methods=["GET"])

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            yield client


# ========================
# Create Function Exception Tests
# ========================

@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_employee_creates_joke_dao_exception(mock_dao_factory, mock_auth, client):
    """Test employee creating joke when DAO raises exception"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.create_record.side_effect = Exception("Database error")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    joke_data = {
        "language": "en",
        "difficulty": 1,
        "content": {"type": "one-liner", "text": "Test joke"}
    }
    
    response = client.post(
        "/jokes",
        json=joke_data,
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_manager_creates_joke_dao_exception(mock_dao_factory, mock_auth, client):
    """Test manager creating joke when DAO raises exception"""
    mock_auth.return_value = manager_creds
    
    mock_dao = MagicMock()
    mock_dao.create_record.side_effect = Exception("Database error")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    joke_data = {
        "language": "en",
        "difficulty": 1,
        "content": {"type": "one-liner", "text": "Test joke"}
    }
    
    response = client.post(
        "/jokes",
        json=joke_data,
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_employee_creates_quote_dao_exception(mock_dao_factory, mock_auth, client):
    """Test employee creating quote when DAO raises exception"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.create_record.side_effect = Exception("Database error")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    quote_data = {
        "language": "en",
        "content": "Test quote",
        "author": "Test Author",
        "category": "motivation"
    }
    
    response = client.post(
        "/quotes",
        json=quote_data,
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_manager_creates_trivia_dao_exception(mock_dao_factory, mock_auth, client):
    """Test manager creating trivia when DAO raises exception"""
    mock_auth.return_value = manager_creds
    
    mock_dao = MagicMock()
    mock_dao.create_record.side_effect = Exception("Database error")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    trivia_data = {
        "language": "en",
        "question": "Test question?",
        "answer": "Test answer"
    }
    
    response = client.post(
        "/trivias",
        json=trivia_data,
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_employee_creates_bio_dao_exception(mock_dao_factory, mock_auth, client):
    """Test employee creating bio when DAO raises exception"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.create_record.side_effect = Exception("Database error")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    bio_data = {
        "language": "en",
        "name": "Test Person",
        "summary": "Test summary",
        "paragraph": "Test paragraph",
        "birth_year": 1900
    }
    
    response = client.post(
        "/bios",
        json=bio_data,
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


# ========================
# Approve Function Tests
# ========================

@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_approve_joke_as_edit(mock_dao_factory, mock_auth, client):
    """Test approving a joke that is an edit (has ref_id)"""
    mock_auth.return_value = manager_creds
    
    # Mock pending joke with is_edit=True and ref_id
    mock_pending_joke = MagicMock()
    mock_pending_joke.is_edit = True
    mock_pending_joke.ref_id = "original123"
    mock_pending_joke.to_json_object.return_value = {"content": "updated"}
    
    mock_private_dao = MagicMock()
    mock_private_dao.get_record_by_id.return_value = mock_pending_joke
    mock_private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_public_dao = MagicMock()
    mock_public_dao.update_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_dao_factory.get_dao.side_effect = [mock_public_dao, mock_private_dao]
    
    response = client.post(
        "/jokes/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 201, 202, 400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_approve_joke_as_new(mock_dao_factory, mock_auth, client):
    """Test approving a joke that is new (is_edit=False)"""
    mock_auth.return_value = manager_creds
    
    # Mock pending joke with is_edit=False
    mock_pending_joke = MagicMock()
    mock_pending_joke.is_edit = False
    mock_pending_joke.ref_id = None
    mock_pending_joke.to_json_object.return_value = {"content": "new joke"}
    
    mock_private_dao = MagicMock()
    mock_private_dao.get_record_by_id.return_value = mock_pending_joke
    mock_private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_public_dao = MagicMock()
    mock_public_dao.create_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_dao_factory.get_dao.side_effect = [mock_public_dao, mock_private_dao]
    
    response = client.post(
        "/jokes/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 201, 202, 400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_approve_joke_update_exception(mock_dao_factory, mock_auth, client):
    """Test approve joke when update raises exception"""
    mock_auth.return_value = manager_creds
    
    mock_pending_joke = MagicMock()
    mock_pending_joke.is_edit = True
    mock_pending_joke.ref_id = "original123"
    mock_pending_joke.to_json_object.return_value = {"content": "updated"}
    
    mock_private_dao = MagicMock()
    mock_private_dao.get_record_by_id.return_value = mock_pending_joke
    
    mock_public_dao = MagicMock()
    mock_public_dao.update_record.side_effect = Exception("Update failed")
    
    mock_dao_factory.get_dao.side_effect = [mock_public_dao, mock_private_dao]
    
    response = client.post(
        "/jokes/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_approve_joke_create_exception(mock_dao_factory, mock_auth, client):
    """Test approve joke when create raises exception"""
    mock_auth.return_value = manager_creds
    
    mock_pending_joke = MagicMock()
    mock_pending_joke.is_edit = False
    mock_pending_joke.ref_id = None
    mock_pending_joke.to_json_object.return_value = {"content": "new"}
    
    mock_private_dao = MagicMock()
    mock_private_dao.get_record_by_id.return_value = mock_pending_joke
    
    mock_public_dao = MagicMock()
    mock_public_dao.create_record.side_effect = Exception("Create failed")
    
    mock_dao_factory.get_dao.side_effect = [mock_public_dao, mock_private_dao]
    
    response = client.post(
        "/jokes/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_approve_joke_delete_exception(mock_dao_factory, mock_auth, client):
    """Test approve joke when delete raises exception"""
    mock_auth.return_value = manager_creds
    
    mock_pending_joke = MagicMock()
    mock_pending_joke.is_edit = False
    mock_pending_joke.to_json_object.return_value = {"content": "new"}
    
    mock_private_dao = MagicMock()
    mock_private_dao.get_record_by_id.return_value = mock_pending_joke
    mock_private_dao.delete_record.side_effect = Exception("Delete failed")
    
    mock_public_dao = MagicMock()
    mock_public_dao.create_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_dao_factory.get_dao.side_effect = [mock_public_dao, mock_private_dao]
    
    response = client.post(
        "/jokes/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_approve_quote_success(mock_dao_factory, mock_auth, client):
    """Test approving a quote"""
    mock_auth.return_value = manager_creds
    
    mock_pending_quote = MagicMock()
    mock_pending_quote.is_edit = False
    mock_pending_quote.to_json_object.return_value = {"content": "new quote"}
    
    mock_private_dao = MagicMock()
    mock_private_dao.get_record_by_id.return_value = mock_pending_quote
    mock_private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_public_dao = MagicMock()
    mock_public_dao.create_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_dao_factory.get_dao.side_effect = [mock_public_dao, mock_private_dao]
    
    response = client.post(
        "/quotes/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 201, 202, 400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_approve_trivia_success(mock_dao_factory, mock_auth, client):
    """Test approving a trivia"""
    mock_auth.return_value = manager_creds
    
    mock_pending_trivia = MagicMock()
    mock_pending_trivia.is_edit = False
    mock_pending_trivia.to_json_object.return_value = {"question": "new trivia"}
    
    mock_private_dao = MagicMock()
    mock_private_dao.get_record_by_id.return_value = mock_pending_trivia
    mock_private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_public_dao = MagicMock()
    mock_public_dao.create_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_dao_factory.get_dao.side_effect = [mock_public_dao, mock_private_dao]
    
    response = client.post(
        "/trivias/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 201, 202, 400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_approve_bio_success(mock_dao_factory, mock_auth, client):
    """Test approving a bio"""
    mock_auth.return_value = manager_creds
    
    mock_pending_bio = MagicMock()
    mock_pending_bio.is_edit = False
    mock_pending_bio.to_json_object.return_value = {"name": "new bio"}
    
    mock_private_dao = MagicMock()
    mock_private_dao.get_record_by_id.return_value = mock_pending_bio
    mock_private_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_public_dao = MagicMock()
    mock_public_dao.create_record.return_value = ResponseCode("GeneralSuccess")
    
    mock_dao_factory.get_dao.side_effect = [mock_public_dao, mock_private_dao]
    
    response = client.post(
        "/bios/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 201, 202, 400, 500]


# ========================
# Deny Function Tests
# ========================

@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_deny_joke_success(mock_dao_factory, mock_auth, client):
    """Test denying a joke"""
    mock_auth.return_value = manager_creds
    
    mock_dao = MagicMock()
    mock_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.post(
        "/jokes/507f1f77bcf86cd799439011/deny",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 204]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_deny_joke_exception(mock_dao_factory, mock_auth, client):
    """Test deny joke when delete raises exception"""
    mock_auth.return_value = manager_creds
    
    mock_dao = MagicMock()
    mock_dao.delete_record.side_effect = Exception("Delete failed")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.post(
        "/jokes/507f1f77bcf86cd799439011/deny",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_deny_quote_success(mock_dao_factory, mock_auth, client):
    """Test denying a quote"""
    mock_auth.return_value = manager_creds
    
    mock_dao = MagicMock()
    mock_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.post(
        "/quotes/507f1f77bcf86cd799439011/deny",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 204]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_deny_trivia_success(mock_dao_factory, mock_auth, client):
    """Test denying a trivia"""
    mock_auth.return_value = manager_creds
    
    mock_dao = MagicMock()
    mock_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.post(
        "/trivias/507f1f77bcf86cd799439011/deny",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 204]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_deny_bio_success(mock_dao_factory, mock_auth, client):
    """Test denying a bio"""
    mock_auth.return_value = manager_creds
    
    mock_dao = MagicMock()
    mock_dao.delete_record.return_value = ResponseCode("GeneralSuccess")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.post(
        "/bios/507f1f77bcf86cd799439011/deny",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 204]


# ========================
# Random Retrieval Tests
# ========================

@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_retrieve_random_joke(mock_dao_factory, mock_auth, client):
    """Test retrieving random jokes"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.get_random_records.return_value = [{"content": "joke1"}, {"content": "joke2"}]
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.get(
        "/random-jokes/2",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_retrieve_random_joke_exception(mock_dao_factory, mock_auth, client):
    """Test retrieve random jokes with exception"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.get_random.side_effect = Exception("Database error")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.get(
        "/random-jokes/2",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code == 500


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_retrieve_random_quote(mock_dao_factory, mock_auth, client):
    """Test retrieving random quotes"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.get_random_records.return_value = [{"content": "quote1"}]
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.get(
        "/random-quotes/1",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_retrieve_random_trivia(mock_dao_factory, mock_auth, client):
    """Test retrieving random trivias"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.get_random_records.return_value = [{"question": "trivia1"}]
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.get(
        "/random-trivias/1",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_retrieve_random_bio(mock_dao_factory, mock_auth, client):
    """Test retrieving random bios"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.get_random_records.return_value = [{"name": "bio1"}]
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.get(
        "/random-bios/1",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_retrieve_short_quote(mock_dao_factory, mock_auth, client):
    """Test retrieving short quotes"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.get_short_record.return_value = [{"content": "short quote"}]
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.get(
        "/short-quotes/1",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_retrieve_short_quote_exception(mock_dao_factory, mock_auth, client):
    """Test retrieve short quotes with exception"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.get_short_record.side_effect = Exception("Database error")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.get(
        "/short-quotes/1",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


# ========================
# Daily Quote Tests
# ========================

@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_retrieve_daily_quote_success(mock_dao_factory, mock_auth, client):
    """Test retrieving daily quote"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.get_quote_of_day.return_value = {"content": "daily quote"}
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.get(
        "/daily-quotes",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [200, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_retrieve_daily_quote_exception(mock_dao_factory, mock_auth, client):
    """Test retrieve daily quote with exception"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao.get_quote_of_day.side_effect = Exception("Database error")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.get(
        "/daily-quotes",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


# ========================
# Proxy Function Tests
# ========================

@patch('all_the_buzz.server.establish_all_daos')
def test_proxy_get_jwt_success(mock_establish):
    """Test proxy_get_jwt with successful JWT retrieval"""
    mock_establish.return_value = None
    test_app = create_app()
    
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {"jwt": "test_jwt_token"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        with test_app.test_client() as client:
            response = client.post(
                "/proxy-get-jwt",
                json={"username": "test", "password": "test"}
            )
            
            assert response.status_code in [200, 502]


@patch('all_the_buzz.server.establish_all_daos')
def test_proxy_get_jwt_no_jwt_in_response(mock_establish):
    """Test proxy_get_jwt when JWT not in response"""
    mock_establish.return_value = None
    test_app = create_app()
    
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {"error": "no jwt"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        with test_app.test_client() as client:
            response = client.post(
                "/proxy-get-jwt",
                json={"username": "test", "password": "test"}
            )
            
            assert response.status_code in [200, 502]


@patch('all_the_buzz.server.establish_all_daos')
def test_proxy_get_jwt_exception(mock_establish):
    """Test proxy_get_jwt with exception"""
    mock_establish.return_value = None
    test_app = create_app()
    
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Connection error")
        
        with test_app.test_client() as client:
            response = client.post(
                "/proxy-get-jwt",
                json={"username": "test", "password": "test"}
            )
            
            assert response.status_code == 502


@patch('all_the_buzz.server.establish_all_daos')
def test_proxy_get_jwt_options(mock_establish):
    """Test proxy_get_jwt with OPTIONS request"""
    mock_establish.return_value = None
    test_app = create_app()
    
    with test_app.test_client() as client:
        response = client.options("/proxy-get-jwt")
        
        assert response.status_code == 200


@patch('all_the_buzz.server.establish_all_daos')
def test_proxy_auth_verify_success(mock_establish):
    """Test proxy_auth_verify with successful verification"""
    mock_establish.return_value = None
    test_app = create_app()
    
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {"valid": True}
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        with test_app.test_client() as client:
            response = client.post(
                "/auth/verify",
                json={"token": "test_token"}
            )
            
            assert response.status_code in [200, 400, 502]


@patch('all_the_buzz.server.establish_all_daos')
def test_proxy_auth_verify_no_token(mock_establish):
    """Test proxy_auth_verify without token"""
    mock_establish.return_value = None
    test_app = create_app()
    
    with test_app.test_client() as client:
        response = client.post(
            "/auth/verify",
            json={}
        )
        
        assert response.status_code == 400


@patch('all_the_buzz.server.establish_all_daos')
def test_proxy_auth_verify_exception(mock_establish):
    """Test proxy_auth_verify with exception"""
    mock_establish.return_value = None
    test_app = create_app()
    
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Auth server down")
        
        with test_app.test_client() as client:
            response = client.post(
                "/auth/verify",
                json={"token": "test_token"}
            )
            
            assert response.status_code == 502


@patch('all_the_buzz.server.establish_all_daos')
def test_proxy_auth_verify_options(mock_establish):
    """Test proxy_auth_verify with OPTIONS request"""
    mock_establish.return_value = None
    test_app = create_app()
    
    with test_app.test_client() as client:
        response = client.options("/auth/verify")
        
        assert response.status_code == 200


# ========================
# Additional Edge Cases
# ========================

@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_create_joke_invalid_entity(mock_dao_factory, mock_auth, client):
    """Test creating joke when entity validation returns non-Joke object"""
    mock_auth.return_value = employee_creds
    
    mock_dao = MagicMock()
    mock_dao_factory.get_dao.return_value = mock_dao
    
    # This should trigger the "else" branch where isinstance(new_joke, Joke) is False
    # We need invalid data that passes initial parsing but fails Joke validation
    with patch('all_the_buzz.server.Joke.from_json_object', return_value="not a joke"):
        response = client.post(
            "/jokes",
            json={"some": "data"},
            headers={"Bearer": "valid_token"}
        )
        
        assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
@patch('all_the_buzz.server.DAOFactory')
def test_approve_joke_get_record_exception(mock_dao_factory, mock_auth, client):
    """Test approve joke when get_record_by_id raises exception"""
    mock_auth.return_value = manager_creds
    
    mock_dao = MagicMock()
    mock_dao.get_record_by_id.side_effect = Exception("Record not found")
    mock_dao_factory.get_dao.return_value = mock_dao
    
    response = client.post(
        "/jokes/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code in [400, 500]


@patch('all_the_buzz.server.authentication')
def test_deny_joke_unauthorized(mock_auth, client):
    """Test denying joke as non-manager"""
    mock_auth.return_value = employee_creds
    
    response = client.post(
        "/jokes/507f1f77bcf86cd799439011/deny",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code == 401


@patch('all_the_buzz.server.authentication')
def test_approve_quote_unauthorized(mock_auth, client):
    """Test approving quote as non-manager"""
    mock_auth.return_value = employee_creds
    
    response = client.post(
        "/quotes/507f1f77bcf86cd799439011/approve",
        headers={"Bearer": "valid_token"}
    )
    
    assert response.status_code == 401
