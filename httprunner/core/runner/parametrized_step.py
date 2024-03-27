from typing import Callable

from httprunner.models import (
    TStep,
)
from httprunner.parser import (
    parse_data,
)


def parse_validate_step_parameters(
    step: TStep, step_config_variables: dict, functions: dict
) -> tuple:
    """Parse and validate parameters of specific parametrized step."""
    argnames, argvalues, ids, is_skip_empty_parameter = step.parametrize

    # make sure argnames is a str
    if not isinstance(argnames, str):
        raise TypeError(
            f"type of argnames must be str, but got {type(argnames)}\n"
            f"Hint: use comma to split multiple arguments"
        )

    parsed_argnames = argnames

    # parse data with step_config_variables instead of with step.variables.
    # cannot parse with step.variables for itself may contain variables that was not parsed yet.
    parsed_argvalues = parse_data(argvalues, step_config_variables, functions)
    parsed_ids = parse_data(ids, step_config_variables, functions)

    # empty argvalues are also accepted if `is_skip_empty_parameter` is True
    if is_skip_empty_parameter and not parsed_argvalues:
        return (
            parsed_argnames,
            parsed_argvalues,
            parsed_ids,
            is_skip_empty_parameter,
        )

    if not isinstance(parsed_argvalues, (list, tuple)):
        raise TypeError(
            f"type of argvalues after parsing must be either list or tuple, but got {type(parsed_argvalues)}"
        )

    if not parsed_argvalues:
        raise ValueError(
            "argvalues cannot be an empty list if `is_skip_empty_parameter` was set to False"
        )

    if "," in argnames:
        parsed_argnames = [_.strip() for _ in argnames.split(",")]

        # each element should be a tuple
        for argvalue in parsed_argvalues:
            if not isinstance(argvalue, (tuple, list)):
                raise TypeError(
                    "type of each argvalue-element must be tuple or list if argnames contain comma"
                )

            if len(argvalue) != len(parsed_argnames):
                raise ValueError(
                    "length of each argvalue-element must be equal to argnames if argnames contain comma"
                )

    if parsed_ids is not None:
        if not isinstance(parsed_ids, (list, tuple)):
            raise TypeError(
                f"if ids was specified, it's type must be list or tuple, but got {type(parsed_ids)}"
            )

        if len(parsed_ids) != len(parsed_argvalues):
            raise ValueError(
                "length of ids must be equal to parsed argvalues if ids is a list or tuple"
            )

    return parsed_argnames, parsed_argvalues, parsed_ids, is_skip_empty_parameter


def expand_parametrized_step(
    origin_step: TStep, step_context_variables: dict, functions: dict
) -> list[TStep]:
    """
    Expand one parametrized step.

    :param origin_step: the original step to be expanded
    :param step_context_variables: variables outside of this step
    :param functions: debug talk functions
    """
    # argnames, argvalues, and ids have already been parsed
    (
        argnames,
        argvalues,
        ids,
        is_skip_empty_parameter,
    ) = parse_validate_step_parameters(
        origin_step,
        step_context_variables,
        functions,
    )

    # eliminate 'parametrize' to avoid expanding this step again
    origin_step.parametrize = None

    # skip step if `is_skip_empty_parameter` is True and parsed `argvalues` is empty
    if is_skip_empty_parameter and not argvalues:
        origin_step.skip_if_condition = True
        origin_step.name = f"{origin_step.name} ◀︎此参数化步骤被跳过，因为 is_skip_empty_parameter 为 true 且解析后 argvalues 为空"

        # clear step.variables for they may reference variables defined by `parametrize`
        origin_step.variables = {}
        return [origin_step]

    expanded_steps = []
    for i, argvalue in enumerate(argvalues):
        # convert arguments to step variables
        if isinstance(argnames, list):
            variables = dict(zip(argnames, argvalue))
        else:
            variables = {argnames: argvalue}

        # deep copy step
        expanded_step = origin_step.model_copy(deep=True)

        # store parsed parametrize variables
        expanded_step.parsed_parametrize_vars = variables

        # determine id
        id = i + 1
        if ids:
            if isinstance(ids, (list, tuple)):
                id = ids[i]
            # Note: ids as Callable is not supported yet
            elif isinstance(ids, Callable):
                id = ids()

        # append id to step name
        expanded_step.name += f" - {id}"
        # run request append extractor to step extract by parametrize id
        expanded_step.extract.extend(
            [
                extractor.model_copy(
                    update={"variable_name": f"{extractor.variable_name}_{i+1}"},
                    deep=True,
                )
                for extractor in expanded_step.extract
            ]
        )
        # testcase append StepExport.var_alias_mapping to export by parametrize id
        if expanded_step.export:
            expanded_step.export.var_alias_mapping.update(
                {
                    var_name: f"{var_name}_{i + 1}"
                    for var_name in expanded_step.export.var_names
                }
            )

        expanded_steps.append(expanded_step)

    return expanded_steps
