from all_the_buzz.entities import Quotes
import pytest

"""
This file runs unit tests on setter methods for Quotes entities in: all_the_buzz/entities/record_entities.py
"""

# ----- Test for initalizing valid quote entitities -----
def test_valid_quote():
    quote = Quotes(id="1"*24, ref_id="2"*24, is_edit=False, language="english")
    quote.category = "Computer"
    quote.author = "Billy Bob"
    quote.used_date = "20-04-2025"

    assert quote.category == "Computer".lower()
    assert quote.author == "Billy Bob"
    assert quote.used_date == "04/20/2025"