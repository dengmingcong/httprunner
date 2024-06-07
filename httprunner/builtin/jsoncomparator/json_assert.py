from typing import Union

from httprunner.builtin.jsoncomparator.comparator import JSONComparator


def assert_equals(
    expected: Union[dict, list],
    actual: Union[dict, list],
    is_strict: bool,
    message: str,
) -> None:
    """Assert that the JSON provided matches the expected JSON.

    :param expected: the expected JSON.
    :param actual: the JSON to compare against the expected JSON.
    :param is_strict: compare the JSON strictly or not.
    :param message: the message to display if the assertion fails.
    """
    json_comparator = JSONComparator(is_strict)
    result = json_comparator.compare_json(expected, actual)

    if not result.is_success:
        if message:
            raise AssertionError(f"{message}\n{result.fail_messages}")
        else:
            raise AssertionError(result.fail_messages)
