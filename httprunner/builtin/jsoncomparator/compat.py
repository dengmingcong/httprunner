from typing import Any

from dotwiz import DotWiz


def normalize_dotwiz(value: Any) -> Any:
    """Convert the value to a dict if it is a DotWiz object.

    :param value: The value to convert.
    """
    if isinstance(value, DotWiz):
        return value.to_dict()
    else:
        return value
