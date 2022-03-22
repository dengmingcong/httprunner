"""
Built-in functions used in YAML/JSON testcases.
"""

import collections.abc
import datetime
import random
import string
import time
from typing import Mapping

from httprunner.exceptions import ParamsError


def gen_random_string(str_len):
    """ generate random string with specified length
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len)
    )


def get_timestamp(str_len=13):
    """ get timestamp string, length can only between 0 and 16
    """
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]

    raise ParamsError("timestamp length can only between 0 and 16.")


def get_current_date(fmt="%Y-%m-%d"):
    """ get current date, default format is %Y-%m-%d
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(n_secs):
    """ sleep n seconds
    """
    time.sleep(n_secs)


def update_dict_recursively(d: dict, u: Mapping) -> dict:
    """
    Update a nested dict recursively.

    Reference: https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict_recursively(d.get(k, {}), v)
        else:
            d[k] = v
    return d
