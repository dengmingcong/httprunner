from typing import NoReturn

from httprunner.models import StepData
from httprunner.models import TStep, JMESPathExtractor
from httprunner.parser import parse_data
from httprunner.response import ResponseObject


def extract(step: TStep, resp_obj: ResponseObject, functions: dict) -> dict:
    """Extract from response content and save to variables."""
    # extract
    extractors: list = step.extract

    # parse JMESPath
    # note: do not change variable 'extractors' directly to reduce surprise
    parsed_extractors = []
    for extractor in extractors:
        if isinstance(extractor, JMESPathExtractor):
            if "$" in extractor.expression:
                extractor = extractor.model_copy(deep=True)
                extractor.expression = parse_data(
                    extractor.expression,
                    step.variables,
                    functions,
                )
            parsed_extractors.append(extractor)

    return resp_obj.extract(parsed_extractors)


def export_local_step_variables(step: TStep) -> dict:
    """Export local variables from step request (HTTP request)."""
    export_mapping = {}

    # export local variables to make them usable for steps next
    for var in step.globalize:
        if isinstance(var, dict):
            if len(var) != 1:
                raise ValueError(
                    f"length of dict can only be 1 but got {len(var)} for: {var}"
                )
            local_var_name = list(var.keys())[0]
            export_as = list(var.values())[0]
        else:
            if not isinstance(var, str) or not var:
                raise ValueError(
                    "type of var can only be dict or str, and must not be empty"
                )
            local_var_name = var
            export_as = var

        if local_var_name not in step.variables:
            raise ValueError(
                f"failed to export local step variable {local_var_name}, "
                f"all step variables now: {step.variables.keys()}"
            )

        export_mapping[export_as] = step.variables[local_var_name]

    return export_mapping


def extract_request_variables(
    resp_obj: ResponseObject,
    step: TStep,
    functions: dict,
) -> dict:
    """Extract and export variables from response object."""
    extract_mapping = extract(step, resp_obj, functions)
    step.variables.update(extract_mapping)

    # make local variables global and available for next steps
    extract_mapping.update(export_local_step_variables(step))

    return extract_mapping


def export_extracted_variables(
    step_data: StepData,
    step_context_variables: dict,
    session_variables: dict,
    extract_mapping: dict,
) -> NoReturn:
    """Export variables, including those extracted from response and those exported from request local variables."""
    step_data.export_vars.update(extract_mapping)

    # update step context variables with new extracted variables
    step_context_variables.update(extract_mapping)

    # put extracted variables to session variables for later exporting
    session_variables.update(extract_mapping)
