from httprunner import exceptions
from httprunner.models import TStep
from httprunner.parser import parse_data


def evaluate_with_api(step: TStep, debugtalk_functions: dict) -> dict:
    """
    Extract variables and preset json from api docs object.

    >>> evaluate_with_api(TStep(name="foo"), {...})
    ... {
    ...     "__api": {...},  # evaluated api docs object
    ...     "foo": "foo",  # extracted variables from api docs object
    ...     "__preset_json": {...}  # extracted preset json from api docs object
    ... }
    """
    # preset variables set by api docs object
    api_preset_variables = {}

    # evaluate api docs object
    if step.request_config.api:
        api_object = parse_data(
            step.request_config.api,
            step.variables,
            debugtalk_functions,
        )
        api_preset_variables["__api"] = api_object

        # extract variables from api docs object
        if variable_extractor := step.request_config.variable_extractor:
            # variable_extractor must be a function defined in debugtalk.py if set
            if variable_extractor not in debugtalk_functions:
                raise exceptions.FunctionNotFound(
                    f"function '{variable_extractor}' not found in debugtalk.py"
                )

            # extract variables from api docs object
            api_preset_variables.update(
                debugtalk_functions[variable_extractor](api_object)
            )

        # extract preset json from api docs object
        if preset_json_extractor := step.request_config.preset_json_extractor:
            # preset_json_extractor must be a function defined in debugtalk.py if set
            if preset_json_extractor not in debugtalk_functions:
                raise exceptions.FunctionNotFound(
                    f"function '{preset_json_extractor}' not found in debugtalk.py"
                )

            # extract preset json from api docs object
            api_preset_variables["__preset_json"] = debugtalk_functions[
                preset_json_extractor
            ](api_object)

    return api_preset_variables
