from httprunner.builtin.jsoncomparator.jsonassert import json_contains_v2


def test_string():
    json_contains_v2("Joe", "Joe")
