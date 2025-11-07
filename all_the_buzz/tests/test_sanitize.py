# Copyright (C) 2025 Team White 
# Licensed under the MIT License
# See LICENSE for more details

import pytest
from all_the_buzz.utilities.sanitize import sanitize_json

def test_sanitize_string_html():
    input_str = "<script>alert('hack');</script>Hello"
    result = sanitize_json(input_str)
    assert "<script>" not in result
    assert "Hello" in result

def test_sanitize_string_curly_braces():
    input_str = "Hello {malicious_code}"
    result = sanitize_json(input_str)
    assert "{" not in result
    assert "Hello" in result

def test_sanitize_string_dollar_variable():
    input_str = "Price is $amount"
    result = sanitize_json(input_str)
    assert "$amount" not in result
    assert "Price is" in result

def test_sanitize_dictionary():
    input_dict = {
        "name": "<b>John</b>",
        "bio": "Hello {hack}",
        "price": "$amount"
    }
    result = sanitize_json(input_dict)
    assert result["name"] == "John"
    assert "{" not in result["bio"]
    assert "$" not in result["price"]

def test_sanitize_list():
    input_list = ["<b>Bold</b>", "{hack}", "$var"]
    result = sanitize_json(input_list)
    assert all("<" not in item and "{" not in item and "$" not in item for item in result)

def test_sanitize_non_supported_type():
    input_val = 12345
    result = sanitize_json(input_val)
    assert result == 12345  # unchanged
