from httprunner import exceptions
from httprunner.exceptions import OverrideReservedVariableError
from httprunner.models import TStep
from httprunner.parser import parse_data


def evaluate_resource(
    step: TStep, debugtalk_functions: dict, resource_tuple: tuple
) -> dict:
    """
    Extract variables and preset json from api docs object.

    >>> evaluate_resource(TStep(name="foo"), {...})
    {
        "resource_name": {...},  # evaluated resource
        "foo": "foo",  # extracted variables from resource
        ...
    }
    """
    # preset variables set by resource
    resource_variables = {}

    resource_name, resource, variable_extractor = resource_tuple

    # avoid variable with the name specified by `resource_name` being overwritten
    if resource_name in step.variables:
        raise OverrideReservedVariableError(
            f"variable name `{resource_name}` is reserved, cannot override it (from outer scope)"
        )

    if resource_name in step.request_config.variables:
        raise OverrideReservedVariableError(
            f"variable name `{resource_name}` is reserved, cannot override it (from request config)"
        )

    if resource_name in step.private_variables:
        raise OverrideReservedVariableError(
            f"variable name `{resource_name}` is reserved, cannot override it (from step private variables)"
        )

    resource_object = parse_data(
        resource,
        step.variables,
        debugtalk_functions,
    )

    # one variable with the same name as `resource_name` will be set
    resource_variables[resource_name] = resource_object

    # extract variables from api docs object
    if variable_extractor:
        # variable_extractor must be a function defined in debugtalk.py if set
        if variable_extractor not in debugtalk_functions:
            raise exceptions.FunctionNotFound(
                f"function '{variable_extractor}' not found in debugtalk.py"
            )

        # extract variables from api docs object
        resource_variables.update(
            debugtalk_functions[variable_extractor](resource_object)
        )

    return resource_variables


def evaluate_resources(step: TStep, debugtalk_functions: dict) -> dict:
    """
    Extract variables and preset json from resources.

    >>> evaluate_resources(TStep(name="foo"), {...})
    {
        "resource_name01": {...},  # evaluated resource 01
        "resource_name02": {...},  # evaluated resource 02
        ...  # and so on
        "foo": "foo",  # extracted variables from resources
        ...
    }
    """
    # preset variables set by resource
    resource_variables = {}

    # evaluate resource
    for resource_tuple in step.request_config.resources:
        resource_variables.update(
            evaluate_resource(step, debugtalk_functions, resource_tuple)
        )

    return resource_variables
