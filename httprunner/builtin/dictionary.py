import operator
from functools import reduce


class Hasher(dict):
    def __missing__(self, key):
        """
        Add key and set the corresponding value to new Hasher instance if key is missing.
        """
        value = self[key] = type(self)()
        return value


def get_from_nested_dict(target_dict: dict, *keys):
    """
    Access nested dictionary items via a list of keys.

    If specific key is missing, add the key and set the corresponding value to a new Hasher.
    This behaves like recursively calling dict.get("some_key", {}).
    """
    hasher = Hasher(target_dict)
    return reduce(operator.getitem, keys, hasher)


def is_keys_exist(d: dict, *keys):
    """
    Check if *keys (nested) exists in `d` (dict).

    Reference: https://stackoverflow.com/questions/43491287/elegant-way-to-check-if-a-nested-key-exists-in-a-dict
    """
    if not isinstance(d, dict):
        raise AttributeError("is_keys_exist() expects dict as first argument.")
    if len(keys) == 0:
        raise AttributeError("is_keys_exist() expects at least two arguments.")

    _d = d
    for key in keys:
        try:
            _d = _d[key]
        except KeyError:
            return False
    return True
