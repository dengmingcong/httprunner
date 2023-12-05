from typing import (
    Text,
    Any,
    Union,
    Callable,
    Literal,
    NoReturn,
    Iterable,
    Sequence,
    Optional,
)

from httprunner.builtin import update_dict_recursively
from httprunner.models import (
    TConfig,
    TStep,
    TRequest,
    MethodEnum,
    TestCase,
    StepExport,
    TRequestConfig,
    JMESPathExtractor,
)

Number = Union[int, float]


class Config(object):
    def __init__(self, name: Text):
        self.__name = name
        self.__variables = {}
        self.__base_url = ""
        self.__verify = False
        self.__continue_on_failure = False
        self.__export = []
        self.__weight = 1
        self.__path = None

    @property
    def name(self) -> Text:
        return self.__name

    @property
    def path(self) -> Text:
        return self.__path

    @path.setter
    def path(self, testcase_file_path: Text) -> NoReturn:
        self.__path = testcase_file_path

    @property
    def weight(self) -> int:
        return self.__weight

    def variables(self, **variables) -> "Config":
        self.__variables.update(variables)
        return self

    def base_url(self, base_url: Text) -> "Config":
        self.__base_url = base_url
        return self

    def verify(self, verify: bool) -> "Config":
        self.__verify = verify
        return self

    def continue_on_failure(self) -> "Config":
        self.__continue_on_failure = True
        return self

    def export(self, *export_var_name: Text) -> "Config":
        self.__export.extend(export_var_name)
        return self

    def locust_weight(self, weight: int) -> "Config":
        self.__weight = weight
        return self

    def perform(self) -> TConfig:
        return TConfig(
            name=self.__name,
            base_url=self.__base_url,
            verify=self.__verify,
            variables=self.__variables,
            export=list(set(self.__export)),
            path=self.__path,
            weight=self.__weight,
            continue_on_failure=self.__continue_on_failure,
        )


class StepRequestValidation(object):
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

    def assert_reports_match(
        self, jmespath_expression: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        """
        This assertion method MUST be used in api 'getAccessLog', and param expected_value MUST be an event dict.
        """
        self._step_context.validators.append(
            {"reports_match": [jmespath_expression, expected_value, message]}
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

    def perform(self) -> TStep:
        return self._step_context


class StepRequestExport(object):
    def __init__(self, step_context: TStep):
        self._step_context = step_context

    def variable(
        self, step_var_name: str, export_as: str = None
    ) -> "StepRequestExport":
        """Make local step variables global for steps next."""
        if export_as:
            self._step_context.globalize.append({step_var_name: export_as})
        else:
            self._step_context.globalize.append(step_var_name)
        return self

    def validate(self) -> StepRequestValidation:
        return StepRequestValidation(self._step_context)

    def perform(self) -> TStep:
        return self._step_context


class StepRequestExtraction(object):
    def __init__(self, step_context: TStep):
        self._step_context = step_context

    def clear(self) -> "StepRequestExtraction":
        """Clear extractors already added."""
        self._step_context.extract = []
        return self

    def with_jmespath(
        self, jmespath_expression: Text, var_name: Text, sub_extractor: Callable = None
    ) -> "StepRequestExtraction":
        self._step_context.extract.append(
            JMESPathExtractor(
                variable_name=var_name,
                expression=jmespath_expression,
                sub_extractor=sub_extractor,
            )
        )
        return self

    # def with_regex(self):
    #     # TODO: extract response html with regex
    #     pass
    #
    # def with_jsonpath(self):
    #     # TODO: extract response json with jsonpath
    #     pass

    def export(self) -> StepRequestExport:
        return StepRequestExport(self._step_context)

    def validate(self) -> StepRequestValidation:
        return StepRequestValidation(self._step_context)

    def perform(self) -> TStep:
        return self._step_context


class RequestWithOptionalArgs(object):
    def __init__(self, step_context: TStep):
        self._step_context = step_context

    def with_origin(self, origin: str) -> "RequestWithOptionalArgs":
        """
        Specify actual origin.

        Origin specified by HTTP method or config.base_url will be substituted by this value.
        """
        self._step_context.request.origin = origin
        return self

    def with_params(self, **params) -> "RequestWithOptionalArgs":
        self._step_context.request.params.update(params)
        return self

    def with_headers(self, **headers) -> "RequestWithOptionalArgs":
        self._step_context.request.headers.update(headers)
        return self

    def with_cookies(self, **cookies) -> "RequestWithOptionalArgs":
        self._step_context.request.cookies.update(cookies)
        return self

    def with_data(self, data) -> "RequestWithOptionalArgs":
        self._step_context.request.data = data
        return self

    def with_json(self, req_json) -> "RequestWithOptionalArgs":
        self._step_context.request.req_json = req_json
        return self

    def update_json_object(
        self,
        req_json_update: Union[dict, str],
        is_deep: bool = True,
        is_update_before_parse: bool = True,
    ) -> "RequestWithOptionalArgs":
        """
        Update request.req_json.

        Note:
            call `with_json()` first before calling this method, otherwise an exception will be raised

        :param req_json_update: the data to update with
        :param is_deep: update recursively if True
        :param is_update_before_parse: update `req_json` with `req_json_update` and then parse the result if True,
            this argument only takes effect if both `req_json` and `req_json_update` are dict
        """
        if self._step_context.request.req_json is None:
            self._step_context.request.req_json = {}

        if is_update_before_parse:
            # apply update if both are dict to avoid parsing error
            if isinstance(self._step_context.request.req_json, dict) and isinstance(
                req_json_update, dict
            ):
                if is_deep:
                    update_dict_recursively(
                        self._step_context.request.req_json, req_json_update
                    )
                else:
                    self._step_context.request.req_json.update(req_json_update)
            else:
                self._step_context.request.req_json_update.append(
                    (req_json_update, is_deep)
                )
        else:
            self._step_context.request.req_json_update.append(
                (req_json_update, is_deep)
            )

        return self

    def update_form_data(
        self,
        data_update: Union[dict, str],
        is_deep: bool = True,
        is_update_before_parse: bool = True,
    ) -> "RequestWithOptionalArgs":
        """
        Update 'request.data' if 'request.data' is a JSON object.

        Note:
            call `with_data()` first before calling this method, otherwise an exception will be raised

        :param data_update: the data to update with
        :param is_deep: update recursively if True
        :param is_update_before_parse: update `data` with `data_update` and then parse the result if True,
            this argument only takes effect if both `data` and `data_update` are dict
        """
        if self._step_context.request.data is None:
            self._step_context.request.data = {}

        if is_update_before_parse:
            # apply update if both are dict to avoid parsing error
            if isinstance(self._step_context.request.data, dict) and isinstance(
                data_update, dict
            ):
                if is_deep:
                    update_dict_recursively(
                        self._step_context.request.data, data_update
                    )
                else:
                    self._step_context.request.data.update(data_update)
            else:
                self._step_context.request.data_update.append((data_update, is_deep))
        else:
            self._step_context.request.data_update.append((data_update, is_deep))

        return self

    def set_timeout(self, timeout: float) -> "RequestWithOptionalArgs":
        self._step_context.request.timeout = timeout
        return self

    def set_verify(self, verify: bool) -> "RequestWithOptionalArgs":
        self._step_context.request.verify = verify
        return self

    def set_allow_redirects(self, allow_redirects: bool) -> "RequestWithOptionalArgs":
        self._step_context.request.allow_redirects = allow_redirects
        return self

    def upload(self, **file_info) -> "RequestWithOptionalArgs":
        self._step_context.request.upload.update(file_info)
        return self

    def teardown_hook(
        self, hook: Text, assign_var_name: Text = None
    ) -> "RequestWithOptionalArgs":
        if assign_var_name:
            self._step_context.teardown_hooks.append({assign_var_name: hook})
        else:
            self._step_context.teardown_hooks.append(hook)

        return self

    def extract(self) -> StepRequestExtraction:
        return StepRequestExtraction(self._step_context)

    def export(self) -> StepRequestExport:
        return StepRequestExport(self._step_context)

    def validate(self) -> StepRequestValidation:
        return StepRequestValidation(self._step_context)

    def perform(self) -> TStep:
        return self._step_context


class RunRequestSetupMixin(object):
    """
    Mixin representing setup for RunRequest.

    This class was separated from original RunRequest for new HttpRunnerRequest.
    """

    def __init__(self, name: Text):
        self._step_context = TStep(name=name)

    def parametrize(
        self,
        argnames: str,
        argvalues: Union[str, Iterable[Union[Sequence[object], object]]],
        ids: Optional[Union[str, Iterable]] = None,
        *,
        is_skip_empty_parameter: bool = True
    ) -> "RunRequestSetupMixin":
        """
        Parametrize step.

        :param argnames: A comma-separated string denoting one or more argument names
        :param argvalues: If only one argname was specified argvalues is a list of values.
            If N argnames were specified, argvalues must be a list of N-tuples, where each tuple-element
            specifies a value for its respective argname.
        :param ids: Sequence of ids for argvalues.
        :param is_skip_empty_parameter: skip steps with an empty parameter set
        """
        self._step_context.parametrize = (
            argnames,
            argvalues,
            ids,
            is_skip_empty_parameter,
        )
        return self

    def retry_on_failure(
        self,
        retry_times: int,
        retry_interval: Union[int, float],
        stop_retry_if: Any = None,
    ) -> "RunRequestSetupMixin":
        """
        Retry step until validation passed or max retries reached, or stop retry condition was met.

        :param retry_times: indicate max retried times
        :param retry_interval: sleep between each retry, unit: seconds
        :param stop_retry_if: stop retrying and mark step failed if the condition was met
        """
        self._step_context.retry_times = retry_times
        self._step_context.max_retry_times = retry_times
        self._step_context.retry_interval = retry_interval
        self._step_context.stop_retry_if = stop_retry_if
        return self

    def skip_if(self, condition: Any, reason: str = None) -> "RunRequestSetupMixin":
        self._step_context.skip_on_condition = condition
        self._step_context.skip_reason = reason
        return self

    def skip_unless(self, condition: Any, reason: str = None) -> "RunRequestSetupMixin":
        self._step_context.run_on_condition = condition
        self._step_context.skip_reason = reason
        return self

    def with_variables(self, **variables) -> "RunRequestSetupMixin":
        self._step_context.variables.update(variables)
        return self

    def with_variables_raw(
        self, raw_variables: str, is_deep: bool = True
    ) -> "RunRequestSetupMixin":
        """
        Update step variables with raw_variables.

        :param raw_variables: the variables parsed from raw_variables will be updated to `step.variables`
        :param is_deep: `raw_variables` will be parsed twice if True
        """
        self._step_context.raw_variables = raw_variables
        self._step_context.is_deep_parse_raw_variables = is_deep
        return self

    def setup_hook(
        self, hook: Text, assign_var_name: Text = None
    ) -> "RunRequestSetupMixin":
        if assign_var_name:
            self._step_context.setup_hooks.append({assign_var_name: hook})
        else:
            self._step_context.setup_hooks.append(hook)
        return self


class RunRequest(RunRequestSetupMixin):
    def __init__(self, name: Text):
        super().__init__(name)

    def get(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.GET, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def post(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.POST, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def put(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.PUT, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def head(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.HEAD, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def delete(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.DELETE, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def options(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.OPTIONS, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def patch(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.PATCH, url=url)
        return RequestWithOptionalArgs(self._step_context)


class RequestConfig(object):
    """
    Class representing request config.
    """

    def __init__(self, name: Text):
        self.__name = name
        self.__variables = {}

    def variables(self, **variables) -> "RequestConfig":
        self.__variables.update(variables)
        return self

    def perform(self) -> TRequestConfig:
        return TRequestConfig(
            name=self.__name,
            variables=self.__variables,
        )


class HttpRunnerRequest(RunRequestSetupMixin, RequestWithOptionalArgs):
    """
    Class representing a HttpRunner request.

    The class attribute 'request' will be used as the default TStep.
    """

    config: RequestConfig
    request: Union[
        RequestWithOptionalArgs, StepRequestValidation, StepRequestExtraction
    ]

    def __init_subclass__(cls):
        """Add validation for subclasses."""
        super().__init_subclass__()

        # make sure type of class attributes correct
        if not isinstance(cls.config, RequestConfig):
            raise ValueError("type of request config must be RequestConfig")

        # make sure TStep.request exist and is not None
        if not isinstance(
            cls.request,
            (RequestWithOptionalArgs, StepRequestValidation, StepRequestExtraction),
        ):
            raise ValueError(
                "type of request must be one of "
                "RequestWithOptionalArgs, StepRequestValidation, or StepRequestExtraction"
            )

    def __init__(self, name: Text = None):  # noqa
        # copy() is not needed for Step.perform() will do the copying thing
        step = self.request.perform()  # type: TStep

        # move variables from step.variables to step.private_variables
        step.private_variables = step.variables
        step.variables = {}
        self._step_context = step

        # update name with data of config
        self.__config = self.config.perform()
        self._step_context.name = self.__config.name
        # overwrite name with instance attribute 'name' if existed
        if name:
            self._step_context.name = name

        # save request config for later usage: testcase config variables > request config variables
        self._step_context.request_config = self.__config

    def perform(self) -> TStep:
        return self._step_context


class StepRefCase(object):
    def __init__(self, step_context: TStep):
        self._step_context = step_context

    def teardown_hook(self, hook: Text, assign_var_name: Text = None) -> "StepRefCase":
        if assign_var_name:
            self._step_context.teardown_hooks.append({assign_var_name: hook})
        else:
            self._step_context.teardown_hooks.append(hook)

        return self

    def export(self, *var_names: str, **var_alias_mapping: str) -> "StepRefCase":
        """
        Export Variables from testcase referenced.

        :param var_names: each item of this list will be exported as is
        :param var_alias_mapping: key is the original variable name, value is the variable name that will be exported as
        """
        if not self._step_context.export:
            self._step_context.export = StepExport(
                var_names=var_names, var_alias_mapping=var_alias_mapping
            )
        else:
            self._step_context.export.var_names.extend(var_names)
            self._step_context.export.var_alias_mapping.update(var_alias_mapping)
        return self

    def perform(self) -> TStep:
        return self._step_context


class RunTestCase(object):
    def __init__(self, name: Text):
        self._step_context = TStep(name=name)

    def parametrize(
        self,
        argnames: str,
        argvalues: Union[str, Iterable[Union[Sequence[object], object]]],
        ids: Optional[Union[str, Iterable]] = None,
        *,
        is_skip_empty_parameter: bool = True
    ) -> "RunTestCase":
        """
        Parametrize step.

        :param argnames: A comma-separated string denoting one or more argument names
        :param argvalues: If only one argname was specified argvalues is a list of values.
            If N argnames were specified, argvalues must be a list of N-tuples, where each tuple-element
            specifies a value for its respective argname.
        :param ids: Sequence of ids for argvalues.
        :param is_skip_empty_parameter: skip steps with an empty parameter set
        """
        self._step_context.parametrize = (
            argnames,
            argvalues,
            ids,
            is_skip_empty_parameter,
        )
        return self

    def skip_if(self, condition: Any, reason: str = None) -> "RunTestCase":
        self._step_context.skip_on_condition = condition
        self._step_context.skip_reason = reason
        return self

    def skip_unless(self, condition: Any, reason: str = None) -> "RunTestCase":
        self._step_context.run_on_condition = condition
        self._step_context.skip_reason = reason
        return self

    def with_variables(self, **variables) -> "RunTestCase":
        self._step_context.variables.update(variables)
        return self

    def with_variables_raw(
        self, raw_variables: str, is_deep: bool = True
    ) -> "RunTestCase":
        """
        Update step variables with raw_variables.

        :param raw_variables: the variables parsed from raw_variables will be updated to `step.variables`
        :param is_deep: `raw_variables` will be parsed twice if True
        """
        self._step_context.raw_variables = raw_variables
        self._step_context.is_deep_parse_raw_variables = is_deep
        return self

    def setup_hook(self, hook: Text, assign_var_name: Text = None) -> "RunTestCase":
        if assign_var_name:
            self._step_context.setup_hooks.append({assign_var_name: hook})
        else:
            self._step_context.setup_hooks.append(hook)

        return self

    def call(self, testcase: Callable) -> StepRefCase:
        self._step_context.testcase = testcase
        return StepRefCase(self._step_context)

    def perform(self) -> TStep:
        return self._step_context


class Step(object):
    def __init__(
        self,
        step_context: Union[
            HttpRunnerRequest,
            StepRequestValidation,
            StepRequestExtraction,
            StepRequestExport,
            RequestWithOptionalArgs,
            RunTestCase,
            StepRefCase,
        ],
    ):
        self._step_context = step_context.perform()

    @property
    def request(self) -> TRequest:
        return self._step_context.request

    @property
    def testcase(self) -> TestCase:
        return self._step_context.testcase  # noqa

    def perform(self) -> TStep:
        # fix: parametrized testcase always use the first parameter
        return self._step_context.copy(deep=True)
