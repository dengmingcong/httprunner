from typing import NoReturn

from httprunner.builtin import update_dict_recursively


def update_form(parsed_request_dict: dict) -> NoReturn:
    """
    Update request with data from update_form_data.
    """
    if not (data_update := parsed_request_dict.pop("data_update", [])):
        return

    init_data = parsed_request_dict["data"]

    if not isinstance(init_data, dict):
        raise ValueError(
            f"method `update_form_data()` can only be used when `data` is a dict, "
            f"but got: {type(init_data)}"
        )

    for data_, is_deep in data_update:
        if not isinstance(data_, dict):
            raise ValueError(
                f"the parsed value of argument `data_update` in method `update_json_object()` must a dict, "
                f"but got: {type(data_)}"
            )
        if is_deep:
            update_dict_recursively(init_data, data_)
        else:
            init_data.update(data_)
