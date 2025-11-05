import pytest
from all_the_buzz.utilities.authentication import authentication
from all_the_buzz.entities.credentials_entity import Credentials
from all_the_buzz.utilities.error_handler import ResponseCode


# --- SUCCESS CASE ---
def test_authentication_success(mocker):
    # Mock config file reader
    mocker.patch("all_the_buzz.utilities.authentication.config_file_reader", return_value={
        "uri": "https://fake-auth.com/login",
        "ping_uri": "https://fake-auth.com/ping"
    })

    # Mock sanitize_json
    mocker.patch("all_the_buzz.utilities.authentication.sanitize_json", side_effect=lambda x: x)

    # Mock Token.from_json_object and to_json_object
    mock_token_obj = mocker.Mock()
    mock_token_obj.to_json_object.return_value = {"token": "abc123"}
    mocker.patch("all_the_buzz.utilities.authentication.Token.from_json_object", return_value=mock_token_obj)

    # Mock requests.get (ping)
    mocker.patch("all_the_buzz.utilities.authentication.requests.get", return_value=mocker.Mock(status_code=200))

    # Mock requests.post (auth server)
    mock_post_response = mocker.Mock()
    mock_post_response.text = '{"id":1,"fname":"Alice","lname":"Smith","department":"IT","title":"Manager","location":"HQ"}'
    mocker.patch("all_the_buzz.utilities.authentication.requests.post", return_value=mock_post_response)

    # Mock Credentials.from_json_object
    mock_creds = Credentials(id=1, fname="Alice", lname="Smith", department="IT", title="Manager", location="HQ")
    mocker.patch("all_the_buzz.utilities.authentication.Credentials.from_json_object", return_value=mock_creds)

    result = authentication({"token": "abc123"})
    assert isinstance(result, Credentials)
    assert result.fname == "Alice"
    assert result.title == "Manager"


# --- INVALID TOKEN ---
def test_authentication_invalid_token(mocker):
    mocker.patch("all_the_buzz.utilities.authentication.sanitize_json", side_effect=lambda x: x)
    mocker.patch("all_the_buzz.utilities.authentication.Token.from_json_object", side_effect=ValueError("Invalid token"))

    result = authentication({"token": "bad"})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "InvalidToken"


# --- CONFIG LOAD ERROR ---
def test_authentication_config_load_error(mocker):
    mocker.patch("all_the_buzz.utilities.authentication.sanitize_json", side_effect=lambda x: x)
    mocker.patch("all_the_buzz.utilities.authentication.Token.from_json_object", return_value=mocker.Mock(to_json_object=lambda: {"token": "abc123"}))

    # Simulate config file reader failure
    mocker.patch("all_the_buzz.utilities.authentication.config_file_reader", side_effect=Exception("Config error"))

    result = authentication({"token": "abc123"})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "ConfigLoadError"


# --- SERVER CONNECTION ERROR ---
def test_authentication_server_down(mocker):
    mocker.patch("all_the_buzz.utilities.authentication.config_file_reader", return_value={
        "uri": "https://fake-auth.com/login",
        "ping_uri": "https://fake-auth.com/ping"
    })
    mocker.patch("all_the_buzz.utilities.authentication.sanitize_json", side_effect=lambda x: x)
    mocker.patch("all_the_buzz.utilities.authentication.Token.from_json_object", return_value=mocker.Mock(to_json_object=lambda: {"token": "abc123"}))

    # Simulate server down
    mocker.patch("all_the_buzz.utilities.authentication.requests.get", side_effect=Exception("Server down"))

    result = authentication({"token": "abc123"})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "ServerConnectionError"


# --- AUTH SERVER ERROR ---
def test_authentication_auth_server_error(mocker):
    mocker.patch("all_the_buzz.utilities.authentication.config_file_reader", return_value={
        "uri": "https://fake-auth.com/login",
        "ping_uri": "https://fake-auth.com/ping"
    })
    mocker.patch("all_the_buzz.utilities.authentication.sanitize_json", side_effect=lambda x: x)
    mocker.patch("all_the_buzz.utilities.authentication.Token.from_json_object", return_value=mocker.Mock(to_json_object=lambda: {"token": "abc123"}))
    mocker.patch("all_the_buzz.utilities.authentication.requests.get", return_value=mocker.Mock(status_code=200))

    # Simulate POST failure
    mocker.patch("all_the_buzz.utilities.authentication.requests.post", side_effect=Exception("Auth server error"))

    result = authentication({"token": "abc123"})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "AuthServerError"


# --- UNAUTHORIZED TOKEN ---
def test_authentication_unauthorized_token(mocker):
    mocker.patch("all_the_buzz.utilities.authentication.config_file_reader", return_value={
        "uri": "https://fake-auth.com/login",
        "ping_uri": "https://fake-auth.com/ping"
    })
    mocker.patch("all_the_buzz.utilities.authentication.sanitize_json", side_effect=lambda x: x)
    mocker.patch("all_the_buzz.utilities.authentication.Token.from_json_object", return_value=mocker.Mock(to_json_object=lambda: {"token": "abc123"}))
    mocker.patch("all_the_buzz.utilities.authentication.requests.get", return_value=mocker.Mock(status_code=200))

    mock_post_response = mocker.Mock()
    mock_post_response.text = '{"id":1,"fname":"Alice"}'  # incomplete data
    mocker.patch("all_the_buzz.utilities.authentication.requests.post", return_value=mock_post_response)

    # Simulate Credentials validation failure
    mocker.patch("all_the_buzz.utilities.authentication.Credentials.from_json_object", side_effect=ValueError("Unauthorized"))

    result = authentication({"token": "abc123"})
    assert isinstance(result, ResponseCode)
    assert result.get_error_tag() == "UnauthorizedToken"