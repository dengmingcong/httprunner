"""
Built-in functions used in YAML/JSON testcases.
"""

import collections.abc
import datetime
import json
import random
import string
import time
from typing import Mapping, Any

from httprunner.exceptions import ParamsError


def gen_random_string(str_len):
    """generate random string with specified length"""
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len)
    )


def get_timestamp(str_len=13):
    """get timestamp string, length can only between 0 and 16"""
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]

    raise ParamsError("timestamp length can only between 0 and 16.")


def get_current_date(fmt="%Y-%m-%d"):
    """get current date, default format is %Y-%m-%d"""
    return datetime.datetime.now().strftime(fmt)


def sleep(n_secs):
    """sleep n seconds"""
    time.sleep(n_secs)


def update_dict_recursively(d: dict, u: Mapping) -> dict:
    """
    Update a nested dict recursively.

    Note:
        The original dict object (argument d) will be changed and the returned object is the same with the original one.

    Reference: https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth

    >>> origin_dict = {"a": {"a1": 11, "a2": 12}, "b": 2, "c": 3}
    >>> update_dict = {"a": {"a1": 1}, "b": 12 }
    >>> return_obj = update_dict_recursively(origin_dict, update_dict)
    >>> return_obj
    {'a': {'a1': 1, 'a2': 12}, 'b': 12, 'c': 3}
    >>> origin_dict
    {'a': {'a1': 1, 'a2': 12}, 'b': 12, 'c': 3}
    >>> return_obj is origin_dict
    True
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict_recursively(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def expand_nested_json(target: Any) -> Any:
    """
    Try to convert string part to Python object using json.loads().

    Note:
        The original object (argument target) will be changed and the return object is the same as the original one.

    >>> origin_obj = {"foo": "{\\"bar\\":\\"baz\\"}"}
    >>> return_obj = expand_nested_json(origin_obj)
    >>> return_obj
    {'foo': {'bar': 'baz'}}
    >>> origin_obj
    {'foo': {'bar': 'baz'}}
    >>> return_obj is origin_obj
    True

    >>> expand_nested_json("{\\"bar\\":\\"baz\\"}")
    {'bar': 'baz'}

    Reference: https://stackoverflow.com/questions/5997029/escape-double-quotes-for-json-in-python
    """
    if isinstance(target, dict):
        for k, v in target.items():
            target[k] = expand_nested_json(v)
        return target
    elif isinstance(target, str) and '"' in target:
        try:
            target = json.loads(target)
        except json.decoder.JSONDecodeError:
            return target
        return expand_nested_json(target)
    elif isinstance(target, list):
        decoded_target = []
        for i in target:
            decoded_target.append(expand_nested_json(i))
        return decoded_target
    else:
        return target
