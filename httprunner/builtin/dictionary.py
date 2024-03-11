import operator
from functools import reduce
from typing import Any, Union


def get_from_nested_dict(target_dict: dict, *keys) -> Any:
    """
    Access nested dictionary items via a list of keys.

    Note:
        1. KeyError will be raised if key not found
        2. TypeError will be raised if object is not a dict

    Reference: https://stackoverflow.com/questions/43491287/elegant-way-to-check-if-a-nested-key-exists-in-a-dict
    """
    if not isinstance(target_dict, dict):
        raise AttributeError("get_from_nested_dict() expects dict as first argument.")
    if len(keys) == 0:
        raise AttributeError("get_from_nested_dict() expects at least two arguments.")

    return reduce(operator.getitem, keys, target_dict)


def get_sub_dict(d: Union[dict, object], *keys) -> dict:
    """
    Get a sub-set of dictionary.
    """
    return {key: d[key] for key in keys if key in d}
