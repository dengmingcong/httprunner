from httprunner.builtin.jsoncomparator.util import (
    SALT,
    get_actual_value,
    get_cardinality_mapping,
    is_usable_as_unique_key,
)


def test_get_actual_value():
    assert get_actual_value((True, SALT)) is True
    assert get_actual_value((False, SALT)) is False


def test_get_cardinality_mapping():
    assert get_cardinality_mapping([1, 2, 2, 3, 3, 3]) == {1: 1, 2: 2, 3: 3}
    assert get_cardinality_mapping(["a", "b", "b", "c", "c", "c"]) == {
        "a": 1,
        "b": 2,
        "c": 3,
    }

    # Boolean values are decorated with SALT.
    assert get_cardinality_mapping([True, False, 1, 0]) == {
        (True, SALT): 1,
        (False, SALT): 1,
        1: 1,
        0: 1,
    }

    # None values are acceptable.
    assert get_cardinality_mapping([None, None, None]) == {None: 3}

    # Empty array.
    assert get_cardinality_mapping([]) == {}

    # 1.0 is equal to 1.
    assert get_cardinality_mapping([1.0, 1, 1.10, 1.1]) == {1: 2, 1.1: 2}


def test_is_usable_as_unique_key():
    assert is_usable_as_unique_key("a", [{"a": 1}, {"a": 2}, {"a": 3}])

    # Candidate key does not exist in all items.
    assert not is_usable_as_unique_key("a", [{"a": 1}, {"b": 2}, {"a": 3}])

    # Value is not simple value.
    assert not is_usable_as_unique_key("a", [{"a": {"b": 1}}, {"a": {"b": 2}}])

    # Value duplicates.
    assert not is_usable_as_unique_key("a", [{"a": 1}, {"a": 1}, {"a": 3}])

    # 1 is not equal to "1".
    assert is_usable_as_unique_key("a", [{"a": 1}, {"a": "1"}, {"a": 3}])

    # True is not equal to 1.
    assert is_usable_as_unique_key("a", [{"a": True}, {"a": False}, {"a": 1}, {"a": 0}])

    # Duplicate boolean values.
    assert not is_usable_as_unique_key("a", [{"a": True}, {"a": False}, {"a": True}])

    # 1.0 is equal to 1.
    assert not is_usable_as_unique_key("a", [{"a": 1.0}, {"a": 1}, {"a": 1.1}])

    # None values are acceptable.
    assert not is_usable_as_unique_key("a", [{"a": None}, {"a": None}, {"a": None}])
    assert is_usable_as_unique_key("a", [{"a": None}, {"a": 1}, {"a": 2}])
