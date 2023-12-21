from typing import NoReturn

from httprunner.models import TStep
from httprunner.parser import parse_data


def parse_retry_args(
    step: TStep, step_context_variables: dict, functions: dict
) -> NoReturn:
    """Parse step retry args (retry times and interval)."""
    if not isinstance(step.max_retry_times, str) and not isinstance(
        step.retry_interval, str
    ):
        return

    parsed_max_retry_times = parse_data(
        step.max_retry_times, step_context_variables, functions
    )

    if not isinstance(parsed_max_retry_times, int):
        raise ValueError(
            f"max_retry_times should be int after parsing, but got: {type(parsed_max_retry_times)}"
        )

    parsed_retry_interval = parse_data(
        step.retry_interval, step_context_variables, functions
    )

    if not isinstance(parsed_retry_interval, (int, float)):
        raise ValueError(
            f"retry_interval should be int or float after parsing, but got: {type(parsed_retry_interval)}"
        )

    step.max_retry_times = parsed_max_retry_times
    step.remaining_retry_times = parsed_max_retry_times
    step.retry_interval = parsed_retry_interval
