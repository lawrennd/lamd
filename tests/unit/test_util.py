import pytest
from lamd import util

def test_set_and_get_since_year():
    # Test initial state
    assert util.get_since_year() is None
    # Set a year and check
    util.set_since_year(2020)
    assert util.get_since_year() == 2020
    # Set another year and check
    util.set_since_year(2023)
    assert util.get_since_year() == 2023 