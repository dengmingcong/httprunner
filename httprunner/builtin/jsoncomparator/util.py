from numbers import Number
from typing import Any, Optional


def is_simple_value(value: Any):
    """The value has a simple data type (neither dict nor list).

    JSON simple values are: number, string, boolean, null.

    :param value: the value to check.
    """
    return isinstance(value, (int, float, str, bool)) or value is None


def is_all_simple_values_array(json_array: list) -> bool:
    """Returns True if all items in the array are simple values.

    :param json_array: the array to check.
    """
    for item in json_array:
        if not is_simple_value(item):
            return False

    return True


def is_all_json_objects_array(json_array: list) -> bool:
    """Returns True if all items in the array are JSON objects.

    :param json_array: the array to check.
    """
    for item in json_array:
        if not isinstance(item, dict):
            return False

    return True


def get_actual_value(value: Any) -> Any:
    """If the value is a tuple, return the first element of the tuple."""
    return (
        value[0]
        if isinstance(value, tuple) and value and value[-1] == "__SALT__"
        else value
    )


def get_cardinality_mapping(json_array: list) -> dict:
    """Get a cardinality mapping of the array.

    The key is the item in the array, and the value is the number of occurrences of the item.
    """
    item_to_count_mapping = {}

    for item in json_array:
        # Distinguish between True and 1 as keys.
        if isinstance(item, bool):
            item = (item, "__SALT__")

        item_to_count_mapping[item] = item_to_count_mapping.get(item, 0) + 1

    return item_to_count_mapping


def is_usable_as_unique_key(candidate_key: str, array: list[dict]) -> bool:
    """Returns True if the candidate key can be used as a unique key across all JSON objects in the array.

    The candidate key is usable as a unique key if every element in the array is a JSON object having that key,
    and no two values are the same.

    :param candidate_key: a top-level key in each of the JSON objects, and it should be a simple value.
    :param json_array: the JSON array to check.
    """
    # record the value of the candidate key in every JSON object, if any value appears more than once,
    # the candidate key cannot be used as a unique key.
    seen_values = set()

    for item in array:
        # if any item is not a JSON object, return False
        if not isinstance(item, dict):
            return False

        # if any item does not have the candidate key, return False
        if candidate_key not in item:
            return False

        value = item[candidate_key]
        # only key whose value is simple value can be usable as unique key,
        # and the value should not appear more than once.
        if is_simple_value(value) and value not in seen_values:
            seen_values.add(value)
        else:
            return False

    return True


def find_unique_key(array: list[dict]) -> Optional[str]:
    """Searches for the unique key of the JSON array.

    All items in the array should be JSON objects (dict).

    Example:
    ```python
    array = [{"a": 1, "b": "a"}, {"a": 2}, {"a": 3}, {"a": 4}]
    print(find_unique_key(array))
    >>>
    "a"
    ```

    :param json_array: the JSON array to search.
    :return: the unique key if found, otherwise None.
    """
    for candidate_key in array[0]:
        if is_usable_as_unique_key(candidate_key, array):
            return candidate_key

    return None


def convert_array_of_json_objects_to_mapping(
    array: list[dict], unique_key: str
) -> dict:
    """Converts the array to a mapping.

    The value of the unique key in each JSON object is used as the key in the mapping.
    The value of the mapping is the JSON object itself.

    :param array: the JSON array to convert.
    :param unique_key: the unique key.
    :return: a dict.
    """
    return {item[unique_key]: item for item in array}


def qualify_field_path(prefix: str, field: str) -> str:
    """Qualify the field path."""
    return f"{prefix}.{field}" if prefix else field


def format_unique_key(prefix: str, unique_key: str, unique_key_value: Any) -> str:
    """Format field path to identify which field failed to match.

    :param prefix: the prefix of the field path.
    :param unique_key: the unique key in each JSON object.
    :param unique_key_value: the value of the unique key in each JSON object.
    """
    return f"{prefix}[{unique_key}={unique_key_value}]"


def is_valid_json_type(value: Any) -> bool:
    """Returns True if the value is a valid JSON type.

    JSON simple values are: number, string, boolean, null.
    JSON complex values are: object, array.

    :param value: the value to check.
    """
    return isinstance(value, (int, float, str, bool, dict, list)) or value is None


def is_number_but_not_bool(value: Any) -> bool:
    """Returns True if the value is a number and not a bool.

    Booleans in Python are implemented as a subclass of integers (https://docs.python.org/3/c-api/bool.html),
    so booleans are Number too, we need to distinguish them.
    """
    return (not isinstance(value, bool)) and isinstance(value, Number)
