from typing import (
    Text,
    Any,
    Union,
    Callable,
    Literal,
    Optional,
    Type,
)

from pydantic import BaseModel

from httprunner.core.testcase.config import Config  # noqa
from httprunner.models import (
    TStep,
)

Number = Union[int, float]


class StepRequestValidation(object):
    """Class representing response validation."""

    def __init__(self, step_context: TStep):
        self._step_context = step_context

    def clear(self) -> "StepRequestValidation":
        """Clear all validators added."""
        self._step_context.validators.clear()
        return self

    def assert_equal(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"equal": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_not_equal(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"not_equal": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_greater_than(
        self,
        jmespath_expression: Text,
        expected_value: Union[int, float, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"greater_than": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_less_than(
        self,
        jmespath_expression: Text,
        expected_value: Union[int, float, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"less_than": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_greater_or_equals(
        self,
        jmespath_expression: Text,
        expected_value: Union[int, float, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"greater_or_equals": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_less_or_equals(
        self,
        jmespath_expression: Text,
        expected_value: Union[int, float, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"less_or_equals": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_length_equal(
        self,
        jmespath_expression: Text,
        expected_value: Union[int, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_equal": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_length_greater_than(
        self,
        jmespath_expression: Text,
        expected_value: Union[int, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_greater_than": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_length_less_than(
        self,
        jmespath_expression: Text,
        expected_value: Union[int, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_less_than": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_length_greater_or_equals(
        self,
        jmespath_expression: Text,
        expected_value: Union[int, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_greater_or_equals": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_length_less_or_equals(
        self,
        jmespath_expression: Text,
        expected_value: Union[int, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_less_or_equals": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_string_equals(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"string_equals": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_startswith(
        self, jmespath_expression: Text, expected_value: Text, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"startswith": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_endswith(
        self, jmespath_expression: Text, expected_value: Text, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"endswith": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_regex_match(
        self, jmespath_expression: Text, expected_value: Text, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"regex_match": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_contains(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"contains": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_not_contain(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"not_contain": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_not_contained_by(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"not_contained_by": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_no_keys_duplicate(
        self, jmespath_expression: Text, message: Text = ""
    ) -> "StepRequestValidation":
        """
        Assert no duplicates in the list specified by jmespath_expression.
        """
        self._step_context.validators.append(
            {"no_keys_duplicate": [jmespath_expression, None, message]}
        )
        return self

    def assert_contained_by(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"contained_by": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_type_match(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"type_match": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_json_contains(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        """
        Equivalent to the JSONassert non-strict mode.

        Note:
            `expected_value` 支持以元组的形式向 DeepDiff 传入额外的参数，但需要满足如下规则:
                1. 元组的第 1 个元素表示真正的预期值
                2. 元组的第 2 个元素必须是一个字典。字典的键必须和 `DeepDiff` 的参数一致，当前只支持这些参数：
                    * ignore_string_type_changes - 忽略字符串类型变更
                    * ignore_numeric_type_changes - 忽略数字类型变更
                    * ignore_type_in_groups - 忽略类型变更

            >>> StepRequestValidation.assert_json_contains(
            ...     "body.result", (
            ...         {"foo", "foo", "bar": "bar"},
            ...         {"ignore_string_type_changes": True, "ignore_numeric_type_changes": True}
            ...     )
            ... )

            reference: https://zepworks.com/deepdiff/current/ignore_types_or_values.html
        """
        self._step_context.validators.append(
            {"json_contains": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_json_equal(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        """
        Equivalent to the JSONassert strict mode.

        Note:
            `expected_value` 支持以元组的形式向 DeepDiff 传入额外的参数，但需要满足如下规则:
                1. 元组的第 1 个元素表示真正的预期值
                2. 元组的第 2 个元素必须是一个字典。字典的键必须和 `DeepDiff` 的参数一致，当前只支持这些参数：
                    * ignore_string_type_changes - 忽略字符串类型变更
                    * ignore_numeric_type_changes - 忽略数字类型变更
                    * ignore_type_in_groups - 忽略类型变更

            >>> StepRequestValidation.assert_json_equal(
            ...     "body.result", (
            ...         {"foo", "foo", "bar": "bar"},
            ...         {"ignore_string_type_changes": True, "ignore_numeric_type_changes": True}
            ...     )
            ... )

            reference: https://zepworks.com/deepdiff/current/ignore_types_or_values.html
        """
        self._step_context.validators.append(
            {"json_equal": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_json_contains_with_java(
        self,
        jmespath_expression: Text,
        expected_value: Any,
        message: Text = "",
    ) -> "StepRequestValidation":
        """Equivalent to the JSONassert non-strict mode with java version."""
        self._step_context.validators.append(
            {"json_contains_with_java": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_json_equal_with_java(
        self,
        jmespath_expression: Text,
        expected_value: Any,
        message: Text = "",
    ) -> "StepRequestValidation":
        """Equivalent to the JSONassert strict mode with java version."""
        self._step_context.validators.append(
            {"json_equal_with_java": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_list_sorted_in(
        self,
        jmespath_expression: Text,
        expected_value: Union[Callable, Literal["ASC", "DSC"]],
        message: Text = "",
    ) -> "StepRequestValidation":
        """
        Assert the list is sorted in some specific order.

        Note:
        1. if expected_value is string 'ASC', the list is expected to be sorted in ascending order
        2. if expected_value is string 'DSC', the list is expected to be sorted in descending order
        3. if expected_value is a function object, you must define and import the function, or use a lambda function,
        reference list.sort() for more information.
        """
        self._step_context.validators.append(
            {"list_sorted_in": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_is_close(
        self,
        jmespath_expression: Text,
        expected_value: Union[tuple[Number, Number], str],
        message: Text = "",
    ) -> "StepRequestValidation":
        """
        Return True if the values are close to each other and False otherwise.

        References:
            math.isclose() from https://docs.python.org/3/library/math.html

        :param jmespath_expression: JMESPath search result must be int or float
        :param expected_value: a tuple, the first element is the expected number, the second is the absolute tolerance
        :param message: error message
        """
        self._step_context.validators.append(
            {"is_close": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_all(
        self,
        jmespath_expression: Text,
        expected_value: Optional[Union[Callable, tuple[Callable, dict], str]] = None,
        message: Text = "",
    ):
        """
        Pass `jmespath_expression` searching result to builtin function `all` and assert the result.

        If `expected_value` is callable, searching result will be passed to it first, then pass the result to `all`.
        The callable accepts only one positional argument.
        >>> StepRequestValidation().assert_all("body.result", lambda x: [v is not None for k, v in x.items()])

        If `expected_value` is a tuple, the first element must be callable, the second element must a dict.
        `jmespath_expression` searching result will be pass to the callable as the first positional argument,
        the second dict element will be passed as keyword arguments to the callable.
        >>> def iterable_to_bool(iterable: dict, ignored: list):
        ...    return [v is not None for k, v in iterable.items() if v not in ignored]
        >>> StepRequestValidation().assert_all("body.result", (iterable_to_bool, {"ignored": ["foo", "bar"]}))

        Reference: https://docs.python.org/3/library/functions.html#all
        """
        self._step_context.validators.append(
            {"all_": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_match_json_schema(
        self,
        jmespath_expression: Text,
        expected_value: Union[dict, str],
        message: Text = "",
    ) -> "StepRequestValidation":
        """
        Assert part of response matches the JSON schema.

        >>> schema = {
        ...     "type" : "object",
        ...     "properties" : {
        ...         "price" : {"type" : "number"},
        ...         "name" : {"type" : "string"},
        ...     },
        ... }
        >>> StepRequestValidation().assert_match_json_schema("body.result", schema)
        """
        self._step_context.validators.append(
            {"match_json_schema": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_match_pydantic_model(
        self,
        jmespath_expression: Text,
        expected_value: Union[Type[BaseModel], str],
        message: Text = "",
    ) -> "StepRequestValidation":
        """
        Assert part of response matches the pydantic model.

        Note:
            By default extra attributes will be ignored, you can change the behaviour via config `extra`.
            reference: https://docs.pydantic.dev/2.5/api/config/#pydantic.config.ConfigDict.extra

        >>> class Teacher(BaseModel)
        ...     name: str
        ...     age: int
        >>> class Student(BaseModel)
        ...     name: str
        ...     age: int
        ...     teacher: Teacher
        >>> StepRequestValidation().assert_match_pydantic_model("body.result", Student)
        """
        self._step_context.validators.append(
            {"match_pydantic_model": [jmespath_expression, expected_value, message]}
        )
        return self

    def assert_is_truthy(self, jmespath_expression: Text, message: Text = ""):
        """
        Assert the value is considered true.

        Reference: https://docs.python.org/3/library/stdtypes.html#truth-value-testing
        """
        self._step_context.validators.append(
            {"is_truthy": [jmespath_expression, None, message]}
        )
        return self

    def assert_is_falsy(self, jmespath_expression: Text, message: Text = ""):
        """
        Assert the value is considered false.

        Reference: https://docs.python.org/3/library/stdtypes.html#truth-value-testing
        """
        self._step_context.validators.append(
            {"is_falsy": [jmespath_expression, None, message]}
        )
        return self

    def assert_lambda(
        self,
        jmespath_expression: Text,
        expected_value: Union[Callable, tuple[Callable, dict]],
        message: Text = "",
    ):
        """
        Assert with custom validator.

        The `expected_value` can be a callable or a tuple.
            1. if `expected_value` is callable, the callable should accept only one positional argument.
                the jmespath searching result will be passed to the callable as the first positional argument.
                >>> def custom_validator(response_data: dict):
                ...     assert response_data["foo"] == "bar"
                >>> StepRequestValidation().assert_lambda("body.result", custom_validator)
            2. if `expected_value` is a tuple, the first element must be callable, the second element must a dict.
                the jmespath searching result will be pass to the callable as the first positional argument,
                the second dict element will be passed as keyword arguments to the callable.
                >>> def custom_validator(response_data: dict, **kwargs):
                ...     assert response_data["foo"] == kwargs["expected_value"]
                >>> StepRequestValidation().assert_lambda("body.result", (custom_validator, {"expected_value": "bar"}))
        """
        self._step_context.validators.append(
            {"assert_lambda": [jmespath_expression, expected_value, message]}
        )
        return self

    def perform(self) -> TStep:
        return self._step_context
