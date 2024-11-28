from httprunner.builtin.jsoncomparator.util import (
    SALT,
    get_actual_value,
    get_cardinality_mapping,
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
    assert get_cardinality_mapping([True, False, True, True, False]) == {
        (True, SALT): 3,
        (False, SALT): 2,
    }
    assert get_cardinality_mapping([None, None, None]) == {None: 3}
    assert get_cardinality_mapping([]) == {}
    assert get_cardinality_mapping([1.0, 1, 1.10, 1.1]) == {1: 2, 1.1: 2}
