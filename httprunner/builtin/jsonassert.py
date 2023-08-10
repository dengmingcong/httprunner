from typing import Union, Optional

from deepdiff import DeepDiff
from dotwiz import DotWiz

from httprunner.builtin.jsonassert_formatter import DeepDiffFormatter


def json_assert(
    actual_value: Union[dict, list],
    expect_value: Union[dict, list],
    message: str,
    strict: bool,
    make_assertion: bool = True,
    **deepdiff_kwargs,
) -> Optional[str]:
    """Equivalent to java unit test lib JSONassert."""
    # assert data types of check value and expect value are the same
    if isinstance(expect_value, dict):
        assert isinstance(
            actual_value, dict
        ), f"the type of data is expected to be 'dict', but '{type(actual_value).__name__}' got."

    if isinstance(expect_value, list):
        assert isinstance(
            actual_value, list
        ), f"the type of data is expected to be 'list', but '{type(actual_value).__name__}' got."

    ignore_order = False
    report_repetition = False

    if not strict:
        ignore_order = True
        report_repetition = True

    ignore_type_in_groups = [(dict, DotWiz)]
    if "ignore_type_in_groups" in deepdiff_kwargs:
        ignore_type_in_groups.extend(deepdiff_kwargs.pop("ignore_type_in_groups"))

    ddiff = DeepDiff(
        expect_value,
        actual_value,
        view="tree",
        ignore_order=ignore_order,
        report_repetition=report_repetition,
        cutoff_intersection_for_pairs=1,
        cutoff_distance_for_pairs=1,
        ignore_type_in_groups=ignore_type_in_groups,
        **deepdiff_kwargs,
    )

    formatter = DeepDiffFormatter(strict, ddiff)
    formatter.format()
    formatted_string = formatter.formatted_string

    if not strict and "dictionary_item_added" in ddiff.to_dict().keys():
        ddiff.pop("dictionary_item_added")

    if make_assertion:
        assert len(ddiff) == 0, f"{message}\n{formatted_string}"
    else:
        if len(ddiff) == 0:
            return None
        else:
            return formatted_string


def json_contains(
    check_value: Union[dict, list],
    expect_value: Union[tuple, dict, list],
    message: str = "",
) -> None:
    """
    Equivalent to the non-strict mode of java unit test lib JSONassert.

    Note:
        `expect_value` 支持以元组的形式向 DeepDiff 传入额外的参数，但需要满足如下规则:
            1. 元组的第 1 个元素表示真正的预期值
            2. 元组的第 2 个元素必须是一个字典。字典的键必须和 `DeepDiff` 的参数一致，当前只支持这些参数：
                * ignore_string_type_changes - 忽略字符串类型变更
                * ignore_numeric_type_changes - 忽略数字类型变更
                * ignore_type_in_groups - 忽略类型变更

        reference: https://zepworks.com/deepdiff/current/ignore_types_or_values.html
    """
    deepdiff_kwargs = {}
    if isinstance(expect_value, tuple):
        if not isinstance(expect_value[1], dict):
            raise TypeError(
                "the second element must be a dict if `expect_value` is a tuple"
            )
        expect_value, deepdiff_kwargs = expect_value  # the real expect_value

    return json_assert(
        check_value, expect_value, message, strict=False, **deepdiff_kwargs
    )


def json_equal(
    check_value: Union[dict, list],
    expect_value: Union[tuple, dict, list],
    message: str = "",
) -> None:
    """
    Equivalent to the strict mode of java unit test lib JSONassert.

    Note:
        `expect_value` 支持以元组的形式向 DeepDiff 传入额外的参数，但需要满足如下规则:
            1. 元组的第 1 个元素表示真正的预期值
            2. 元组的第 2 个元素必须是一个字典。字典的键必须和 `DeepDiff` 的参数一致，当前只支持这些参数：
                * ignore_string_type_changes - 忽略字符串类型变更
                * ignore_numeric_type_changes - 忽略数字类型变更
                * ignore_type_in_groups - 忽略类型变更

        reference: https://zepworks.com/deepdiff/current/ignore_types_or_values.html
    """
    deepdiff_kwargs = {}
    if isinstance(expect_value, tuple):
        if not isinstance(expect_value[1], dict):
            raise TypeError(
                "the second element must be a dict if `expect_value` is a tuple"
            )
        expect_value, deepdiff_kwargs = expect_value  # the real expect_value

    return json_assert(
        check_value, expect_value, message, strict=True, **deepdiff_kwargs
    )


def get_json_contains_diff_message(
    check_value: Union[dict, list], expect_value: Union[dict, list], message: str = ""
) -> Optional[str]:
    """
    Return None if check ok, else return formatted string.
    """
    return json_assert(
        check_value, expect_value, message, strict=False, make_assertion=False
    )
