# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details

import pytest
from unittest.mock import MagicMock
from all_the_buzz.database_operations.bios_dao import PublicBioDAO, PrivateBioDAO
from all_the_buzz.database_operations.jokes_dao import PublicJokeDAO, PrivateJokeDAO
from all_the_buzz.database_operations.trivia_dao import PublicTriviaDAO, PrivateTriviaDAO
from all_the_buzz.entities.credentials_entity import Credentials

"""
Unit tests for DAO classes (Bios, Jokes, Trivia).
These tests verify the initialization and role matrices of DAO classes.
"""

# Fixtures
@pytest.fixture
def mock_client():
    """Create a mock MongoDB client."""
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection
    return mock_client

@pytest.fixture
def manager_credentials():
    """Create manager credentials."""
    return Credentials(
        id=1,
        fName="Alice",
        lName="Manager",
        dept="IT",
        title="Manager",
        loc="HQ"
    )

@pytest.fixture
def employee_credentials():
    """Create employee credentials."""
    return Credentials(
        id=2,
        fName="Bob",
        lName="Employee",
        dept="IT",
        title="Developer",
        loc="HQ"
    )

# --- PublicBioDAO Tests ---
def test_public_bio_dao_initialization(mock_client):
    """Test that PublicBioDAO initializes correctly."""
    dao = PublicBioDAO(mock_client, "test_db")
    assert dao is not None
    assert dao._collection is not None

def test_public_bio_dao_role_matrix():
    """Test that PublicBioDAO has correct role matrix."""
    expected_matrix = {
        "read": ["Employee", "Manager"],
        "create": ["Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }
    assert PublicBioDAO.ROLE_MATRIX == expected_matrix

def test_public_bio_dao_table_name(mock_client):
    """Test that PublicBioDAO connects to correct collection."""
    dao = PublicBioDAO(mock_client, "test_db")
    # Verify it tried to get the right collection
    mock_client.__getitem__.assert_called_with("test_db")

# --- PrivateBioDAO Tests ---
def test_private_bio_dao_initialization(mock_client):
    """Test that PrivateBioDAO initializes correctly."""
    dao = PrivateBioDAO(mock_client, "test_db")
    assert dao is not None
    assert dao._collection is not None

def test_private_bio_dao_role_matrix():
    """Test that PrivateBioDAO has correct role matrix."""
    expected_matrix = {
        "read": ["Manager"],
        "create": ["Employee", "Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }
    assert PrivateBioDAO.ROLE_MATRIX == expected_matrix

# --- PublicJokeDAO Tests ---
def test_public_joke_dao_initialization(mock_client):
    """Test that PublicJokeDAO initializes correctly."""
    dao = PublicJokeDAO(mock_client, "test_db")
    assert dao is not None
    assert dao._collection is not None

def test_public_joke_dao_role_matrix():
    """Test that PublicJokeDAO has correct role matrix."""
    expected_matrix = {
        "read": ["Employee", "Manager"],
        "create": ["Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }
    assert PublicJokeDAO.ROLE_MATRIX == expected_matrix

# --- PrivateJokeDAO Tests ---
def test_private_joke_dao_initialization(mock_client):
    """Test that PrivateJokeDAO initializes correctly."""
    dao = PrivateJokeDAO(mock_client, "test_db")
    assert dao is not None
    assert dao._collection is not None

def test_private_joke_dao_role_matrix():
    """Test that PrivateJokeDAO has correct role matrix."""
    expected_matrix = {
        "read": ["Manager"],
        "create": ["Employee", "Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }
    assert PrivateJokeDAO.ROLE_MATRIX == expected_matrix

# --- PublicTriviaDAO Tests ---
def test_public_trivia_dao_initialization(mock_client):
    """Test that PublicTriviaDAO initializes correctly."""
    dao = PublicTriviaDAO(mock_client, "test_db")
    assert dao is not None
    assert dao._collection is not None

def test_public_trivia_dao_role_matrix():
    """Test that PublicTriviaDAO has correct role matrix."""
    expected_matrix = {
        "read": ["Employee", "Manager"],
        "create": ["Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }
    assert PublicTriviaDAO.ROLE_MATRIX == expected_matrix

# --- PrivateTriviaDAO Tests ---
def test_private_trivia_dao_initialization(mock_client):
    """Test that PrivateTriviaDAO initializes correctly."""
    dao = PrivateTriviaDAO(mock_client, "test_db")
    assert dao is not None
    assert dao._collection is not None

def test_private_trivia_dao_role_matrix():
    """Test that PrivateTriviaDAO has correct role matrix."""
    expected_matrix = {
        "read": ["Manager"],
        "create": ["Employee", "Manager"],
        "update": ["Manager"],
        "delete": ["Manager"]
    }
    assert PrivateTriviaDAO.ROLE_MATRIX == expected_matrix

# --- Cross-DAO Consistency Tests ---
def test_all_public_daos_allow_employee_read():
    """Test that all public DAOs allow employees to read."""
    public_daos = [PublicBioDAO, PublicJokeDAO, PublicTriviaDAO]

    for dao_class in public_daos:
        assert "Employee" in dao_class.ROLE_MATRIX["read"]
        assert "Manager" in dao_class.ROLE_MATRIX["read"]

def test_all_private_daos_restrict_read_to_manager():
    """Test that all private DAOs restrict read access to managers only."""
    private_daos = [PrivateBioDAO, PrivateJokeDAO, PrivateTriviaDAO]

    for dao_class in private_daos:
        assert dao_class.ROLE_MATRIX["read"] == ["Manager"]

def test_all_private_daos_allow_employee_create():
    """Test that all private DAOs allow employees to create."""
    private_daos = [PrivateBioDAO, PrivateJokeDAO, PrivateTriviaDAO]

    for dao_class in private_daos:
        assert "Employee" in dao_class.ROLE_MATRIX["create"]
        assert "Manager" in dao_class.ROLE_MATRIX["create"]

def test_all_daos_restrict_update_to_manager():
    """Test that all DAOs restrict update to managers only."""
    all_daos = [
        PublicBioDAO, PrivateBioDAO,
        PublicJokeDAO, PrivateJokeDAO,
        PublicTriviaDAO, PrivateTriviaDAO
    ]

    for dao_class in all_daos:
        assert dao_class.ROLE_MATRIX["update"] == ["Manager"]

def test_all_daos_restrict_delete_to_manager():
    """Test that all DAOs restrict delete to managers only."""
    all_daos = [
        PublicBioDAO, PrivateBioDAO,
        PublicJokeDAO, PrivateJokeDAO,
        PublicTriviaDAO, PrivateTriviaDAO
    ]

    for dao_class in all_daos:
        assert dao_class.ROLE_MATRIX["delete"] == ["Manager"]

def test_dao_inheritance():
    """Test that all DAO classes properly inherit from DatabaseAccessObject."""
    from all_the_buzz.database_operations.abstract_record import DatabaseAccessObject

    all_daos = [
        PublicBioDAO, PrivateBioDAO,
        PublicJokeDAO, PrivateJokeDAO,
        PublicTriviaDAO, PrivateTriviaDAO
    ]

    for dao_class in all_daos:
        assert issubclass(dao_class, DatabaseAccessObject)
