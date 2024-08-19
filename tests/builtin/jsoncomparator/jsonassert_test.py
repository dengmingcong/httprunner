import pytest

from httprunner.builtin.jsoncomparator.jsonassert import json_contains_v2


def test_string():
    with pytest.raises(AssertionError):
        json_contains_v2("Joe", "Joe")
