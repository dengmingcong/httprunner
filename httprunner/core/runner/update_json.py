from typing import NoReturn

from httprunner.builtin import update_dict_recursively


def update_json(parsed_request_dict: dict) -> NoReturn:
    """
    Update request with data from update_json_object.
    """
    # skip if `req_json_update` is empty
    if not (req_json_update := parsed_request_dict.pop("req_json_update", [])):
        return

    req_json = parsed_request_dict["req_json"]

    if not isinstance(req_json, dict):
        raise ValueError(
            f"method `update_json_object()` can only be used when `req_json` (after parsing) is a dict, "
            f"but got: {type(req_json)}"
        )

    for update_data, is_deep in req_json_update:
        if not isinstance(update_data, dict):
            raise ValueError(
                f"the parsed value of argument `req_json_update` in method `update_json_object()` must a dict, "
                f"but got: {type(req_json)}"
            )
        if is_deep:
            update_dict_recursively(req_json, update_data)
        else:
            req_json.update(update_data)
