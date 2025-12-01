# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details

import pytest
import tempfile
import os
from all_the_buzz.utilities.config import config_file_reader

"""
Unit tests for config.py utility functions.
These tests actually test the functionality of loading YAML config files.
"""

def test_config_file_reader_valid_yaml():
    """Test that config_file_reader correctly reads a valid YAML file."""
    # Create a temporary YAML file
    yaml_content = """
database:
  host: localhost
  port: 27017
  name: test_db
auth:
  enabled: true
  timeout: 30
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        # Read the config file
        result = config_file_reader(temp_path)

        # Verify the structure and values
        assert isinstance(result, dict)
        assert 'database' in result
        assert result['database']['host'] == 'localhost'
        assert result['database']['port'] == 27017
        assert result['database']['name'] == 'test_db'
        assert 'auth' in result
        assert result['auth']['enabled'] is True
        assert result['auth']['timeout'] == 30
    finally:
        # Clean up
        os.unlink(temp_path)

def test_config_file_reader_empty_yaml():
    """Test that config_file_reader handles an empty YAML file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("")
        temp_path = f.name

    try:
        result = config_file_reader(temp_path)
        # Empty YAML file should return None
        assert result is None
    finally:
        os.unlink(temp_path)

def test_config_file_reader_nested_structure():
    """Test that config_file_reader correctly reads nested YAML structures."""
    yaml_content = """
app:
  name: TestApp
  settings:
    debug: true
    logging:
      level: INFO
      file: app.log
    features:
      - feature1
      - feature2
      - feature3
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        result = config_file_reader(temp_path)

        # Verify nested structure
        assert result['app']['name'] == 'TestApp'
        assert result['app']['settings']['debug'] is True
        assert result['app']['settings']['logging']['level'] == 'INFO'
        assert result['app']['settings']['logging']['file'] == 'app.log'
        assert isinstance(result['app']['settings']['features'], list)
        assert len(result['app']['settings']['features']) == 3
        assert 'feature1' in result['app']['settings']['features']
    finally:
        os.unlink(temp_path)

def test_config_file_reader_file_not_found():
    """Test that config_file_reader raises FileNotFoundError for non-existent file."""
    with pytest.raises(FileNotFoundError):
        config_file_reader("/non/existent/path/config.yaml")

def test_config_file_reader_invalid_yaml():
    """Test that config_file_reader raises an error for invalid YAML syntax."""
    invalid_yaml = """
key1: value1
  key2: value2
    invalid indentation
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(invalid_yaml)
        temp_path = f.name

    try:
        with pytest.raises(Exception):  # YAML parsing will raise an exception
            config_file_reader(temp_path)
    finally:
        os.unlink(temp_path)

def test_config_file_reader_with_lists():
    """Test that config_file_reader correctly handles YAML lists."""
    yaml_content = """
servers:
  - name: server1
    ip: 192.168.1.1
  - name: server2
    ip: 192.168.1.2
ports:
  - 8080
  - 8081
  - 8082
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        result = config_file_reader(temp_path)

        assert isinstance(result['servers'], list)
        assert len(result['servers']) == 2
        assert result['servers'][0]['name'] == 'server1'
        assert result['servers'][1]['ip'] == '192.168.1.2'
        assert isinstance(result['ports'], list)
        assert 8080 in result['ports']
    finally:
        os.unlink(temp_path)

def test_config_file_reader_mixed_types():
    """Test that config_file_reader handles mixed data types correctly."""
    yaml_content = """
string_value: "test"
integer_value: 42
float_value: 3.14
boolean_true: true
boolean_false: false
null_value: null
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name

    try:
        result = config_file_reader(temp_path)

        assert result['string_value'] == 'test'
        assert result['integer_value'] == 42
        assert result['float_value'] == 3.14
        assert result['boolean_true'] is True
        assert result['boolean_false'] is False
        assert result['null_value'] is None
    finally:
        os.unlink(temp_path)
