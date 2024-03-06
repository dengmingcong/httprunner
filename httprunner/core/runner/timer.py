from typing import NoReturn

from httprunner.models import TStep
from httprunner.parser import parse_data


def display_delay_in_step_name(step: TStep, functions: dict) -> NoReturn:
    """Display delay in step name."""
    delay_messages = []

    # display delay before running step
    if step.pre_delay_seconds:
        step.pre_delay_seconds = parse_data(step.pre_delay_seconds, functions)

        # pre_delay_seconds must be int or float
        if not isinstance(step.pre_delay_seconds, (int, float)):
            raise TypeError(
                f"pre_delay_seconds must be int or float, got {type(step.pre_delay_seconds)}"
            )

        if step.pre_delay_seconds:
            delay_messages.append(f"Delay Before: {step.pre_delay_seconds} seconds")

    # display delay after running step
    if step.post_delay_seconds:
        step.post_delay_seconds = parse_data(step.post_delay_seconds, functions)

        # post_delay_seconds must be int or float
        if not isinstance(step.post_delay_seconds, (int, float)):
            raise TypeError(
                f"post_delay_seconds must be int or float, got {type(step.post_delay_seconds)}"
            )

        if step.post_delay_seconds:
            delay_messages.append(f"Delay After: {step.post_delay_seconds} seconds")

    # join delay messages with '/', and display at the end of step name (separated by icon ⏱️)
    if delay_messages:
        step.name = f"{step.name} ⏱️ {' / '.join(delay_messages)}"
