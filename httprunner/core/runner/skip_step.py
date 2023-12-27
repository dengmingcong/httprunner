from loguru import logger

from httprunner.models import TStep
from httprunner.parser import parse_data


def is_skip_step(step: TStep, step_context_variables: dict, functions: dict) -> bool:
    """Handle when skip_if or skip_unless was set."""
    # skip_if and skip_unless can not be set at the same time
    if step.skip_if_condition is not None and step.skip_unless_condition is not None:
        raise SyntaxError("skip_if and skip_unless can not be set at the same time")

    # both skip_if and skip_unless were not set
    if step.skip_if_condition is None and step.skip_unless_condition is None:
        return False

    # skip_if was set
    if step.skip_if_condition is not None:
        parsed_skip_condition = parse_data(
            step.skip_if_condition,
            step_context_variables,
            functions,
        )
        logger.debug(
            f"parsed skip condition: {parsed_skip_condition} ({type(parsed_skip_condition)})"
        )

        # call `eval()` if type is str
        if isinstance(parsed_skip_condition, str):
            parsed_skip_condition = eval(parsed_skip_condition)

        if parsed_skip_condition:
            parsed_skip_reason = parse_data(
                step.skip_reason,
                step_context_variables,
                functions,
            )
            logger.info(f"skip condition was met, reason: {parsed_skip_reason}")
            return True
        else:
            logger.info("skip condition was not met, run the step")
            return False

    # skip_unless was set
    if step.skip_unless_condition is not None:
        parsed_run_condition = parse_data(
            step.skip_unless_condition,
            step_context_variables,
            functions,
        )
        logger.debug(
            f"parsed run condition: {parsed_run_condition} ({type(parsed_run_condition)})"
        )

        # eval again if type is str
        if isinstance(parsed_run_condition, str):
            parsed_run_condition = eval(parsed_run_condition)

        if not parsed_run_condition:
            parsed_skip_reason = parse_data(
                step.skip_reason,
                step_context_variables,
                functions,
            )
            logger.info(f"skip condition was met, reason: {parsed_skip_reason}")
            return True
        else:
            logger.info("run condition was met, run the step")
            return False
