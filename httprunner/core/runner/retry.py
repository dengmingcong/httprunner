from typing import NoReturn

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


def gen_retry_step_title(step: TStep, is_validation_pass: bool, functions: dict, content_length: int) -> str:
    """Generate retry step title."""
    if is_validation_pass:
        emoji = emojis.success
    else:
        emoji = emojis.failure

    if step.max_retry_times == step.remaining_retry_times:
        title = f"first request {emoji}"
    elif step.remaining_retry_times == 0:
        title = f"retry: {step.max_retry_times} - last retry {emoji}"
    else:
        title = f"retry: {step.max_retry_times - step.remaining_retry_times} {emoji}"

    if step.stop_retry_if is not None and parse_data(
        step.stop_retry_if, step.variables, functions
    ):
        title += " (the condition to stop retrying was met)"

    title += f'  • Content-Length: {content_length}'

    return title
