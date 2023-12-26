from typing import NoReturn

from loguru import logger

from httprunner.configs.emoji import emojis
from httprunner.models import TStep
from httprunner.parser import parse_data


def parse_retry_args(
    step: TStep, step_context_variables: dict, functions: dict
) -> NoReturn:
    """Parse step retry args (retry_times and retry_interval)."""
    # parse retry_times
    if isinstance(step.max_retry_times, str):
        parsed_max_retry_times = parse_data(
            step.max_retry_times, step_context_variables, functions
        )

        if not isinstance(parsed_max_retry_times, int):
            raise ValueError(
                f"max_retry_times should be int after parsing, but got: {type(parsed_max_retry_times)}"
            )
        step.max_retry_times = parsed_max_retry_times
        step.remaining_retry_times = parsed_max_retry_times

    if isinstance(step.retry_interval, str):
        parsed_retry_interval = parse_data(
            step.retry_interval, step_context_variables, functions
        )

        if not isinstance(parsed_retry_interval, (int, float)):
            raise ValueError(
                f"retry_interval should be int or float after parsing, but got: {type(parsed_retry_interval)}"
            )

        step.retry_interval = parsed_retry_interval


def is_meet_stop_retry_condition(step: TStep, functions: dict) -> bool:
    """Return True if meet stop retry condition, otherwise False."""
    if step.stop_retry_if is None:
        return False

    parsed_stop_retry_condition = parse_data(
        step.stop_retry_if, step.variables, functions
    )

    logger.debug(
        f"parsed stop retry condition: {parsed_stop_retry_condition} ({type(parsed_stop_retry_condition)})"
    )

    if isinstance(parsed_stop_retry_condition, str):
        parsed_stop_retry_condition = eval(parsed_stop_retry_condition)
        logger.debug(f"eval parsed stop retry condition: {parsed_stop_retry_condition}")

    return bool(parsed_stop_retry_condition)


def gen_retry_step_title(
    step: TStep, is_pass: bool, content_length: int, is_stop_retry: bool
) -> str:
    """Generate retry step title."""
    if is_pass:
        emoji = emojis.success
    else:
        emoji = emojis.failure

    if step.max_retry_times == step.remaining_retry_times:
        title = f"first request {emoji}"
    elif step.remaining_retry_times == 0:
        title = f"retry: {step.max_retry_times} - last retry {emoji}"
    else:
        title = f"retry: {step.max_retry_times - step.remaining_retry_times} {emoji}"

    if is_stop_retry:
        title += " (the condition to stop retrying was met)"

    title += f"  • Content-Length: {content_length}"

    return title
