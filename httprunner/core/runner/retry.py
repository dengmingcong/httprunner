from typing import NoReturn

from loguru import logger

from httprunner.configs.emoji import emojis
from httprunner.exceptions import ValidationFailure
from httprunner.models import TStep
from httprunner.parser import parse_data


def parse_retry_args(
    step: TStep, step_shell_variables: dict, functions: dict
) -> NoReturn:
    """Parse step retry args (retry_times and retry_interval)."""
    if step.is_retry_args_resolved:
        return

    # parse retry_times
    if isinstance(step.max_retry_times, str):
        parsed_max_retry_times = parse_data(
            step.max_retry_times, step_shell_variables, functions
        )

        step.max_retry_times = int(parsed_max_retry_times)
        step.remaining_retry_times = int(parsed_max_retry_times)

    if isinstance(step.retry_interval, str):
        parsed_retry_interval = parse_data(
            step.retry_interval, step_shell_variables, functions
        )

        step.retry_interval = float(parsed_retry_interval)

    step.is_retry_args_resolved = True


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


def is_final_request(step: TStep, functions: dict, exception: Exception) -> bool:
    """Return True if this is the final request (no more retrying will be executed)."""
    # success will stop retrying automatically
    if not exception:
        return True

    # exception other than ValidationFailure will stop retrying automatically
    if not isinstance(exception, ValidationFailure):
        return True

    # this request will become last retry if stopping retrying condition was met
    if is_meet_stop_retry_condition(step, functions):
        return True

    # this request will become last retry if remaining retry times is 0
    if step.remaining_retry_times == 0:
        return True

    return False
