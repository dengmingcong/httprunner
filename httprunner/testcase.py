import inspect
from typing import Text, Any, Union, Callable, Literal

from httprunner.models import (
    TConfig,
    TStep,
    TRequest,
    MethodEnum,
    TestCase,
    StepExport,
    TRequestConfig,
)


class Config(object):
    def __init__(self, name: Text):
        self.__name = name
        self.__variables = {}
        self.__base_url = ""
        self.__verify = False
        self.__continue_on_failure = False
        self.__export = []
        self.__weight = 1

        caller_frame = inspect.stack()[1]
        self.__path = caller_frame.filename

    @property
    def name(self) -> Text:
        return self.__name

    @property
    def path(self) -> Text:
        return self.__path

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
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"equal": [jmes_path, expected_value, message]}
        )
        return self

    def assert_not_equal(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"not_equal": [jmes_path, expected_value, message]}
        )
        return self

    def assert_greater_than(
        self, jmes_path: Text, expected_value: Union[int, float, str], message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"greater_than": [jmes_path, expected_value, message]}
        )
        return self

    def assert_less_than(
        self, jmes_path: Text, expected_value: Union[int, float, str], message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"less_than": [jmes_path, expected_value, message]}
        )
        return self

    def assert_greater_or_equals(
        self, jmes_path: Text, expected_value: Union[int, float, str], message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"greater_or_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_less_or_equals(
        self, jmes_path: Text, expected_value: Union[int, float, str], message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"less_or_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_equal(
        self, jmes_path: Text, expected_value: Union[int, str], message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_equal": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_greater_than(
        self, jmes_path: Text, expected_value: Union[int, str], message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_greater_than": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_less_than(
        self, jmes_path: Text, expected_value: Union[int, str], message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_less_than": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_greater_or_equals(
        self, jmes_path: Text, expected_value: Union[int, str], message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_greater_or_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_length_less_or_equals(
        self, jmes_path: Text, expected_value: Union[int, str], message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"length_less_or_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_string_equals(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"string_equals": [jmes_path, expected_value, message]}
        )
        return self

    def assert_startswith(
        self, jmes_path: Text, expected_value: Text, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"startswith": [jmes_path, expected_value, message]}
        )
        return self

    def assert_endswith(
        self, jmes_path: Text, expected_value: Text, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"endswith": [jmes_path, expected_value, message]}
        )
        return self

    def assert_regex_match(
        self, jmes_path: Text, expected_value: Text, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"regex_match": [jmes_path, expected_value, message]}
        )
        return self

    def assert_contains(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"contains": [jmes_path, expected_value, message]}
        )
        return self

    def assert_not_contain(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"not_contain": [jmes_path, expected_value, message]}
        )
        return self

    def assert_not_contained_by(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"not_contained_by": [jmes_path, expected_value, message]}
        )
        return self

    def assert_no_keys_duplicate(
        self, jmes_path: Text, message: Text = ""
    ) -> "StepRequestValidation":
        """
        断言 list 中是否含有重复的元素
        """
        self._step_context.validators.append(
            {"no_keys_duplicate": [jmes_path, None, message]}
        )
        return self

    def assert_contained_by(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"contained_by": [jmes_path, expected_value, message]}
        )
        return self

    def assert_type_match(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        self._step_context.validators.append(
            {"type_match": [jmes_path, expected_value, message]}
        )
        return self

    def assert_json_contains(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        """Equivalent to the JSONassert non-strict mode."""
        self._step_context.validators.append(
            {"json_contains": [jmes_path, expected_value, message]}
        )
        return self

    def assert_json_equal(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        """Equivalent to the JSONassert strict mode."""
        self._step_context.validators.append(
            {"json_equal": [jmes_path, expected_value, message]}
        )
        return self

    def assert_json_contains_with_java(
        self,
        jmes_path: Text,
        expected_value: Any,
        message: Text = "",
    ) -> "StepRequestValidation":
        """Equivalent to the JSONassert non-strict mode with java version."""
        self._step_context.validators.append(
            {"json_contains_with_java": [jmes_path, expected_value, message]}
        )
        return self

    def assert_json_equal_with_java(
        self,
        jmes_path: Text,
        expected_value: Any,
        message: Text = "",
    ) -> "StepRequestValidation":
        """Equivalent to the JSONassert strict mode with java version."""
        self._step_context.validators.append(
            {"json_equal_with_java": [jmes_path, expected_value, message]}
        )
        return self

    def assert_reports_match(
        self, jmes_path: Text, expected_value: Any, message: Text = ""
    ) -> "StepRequestValidation":
        """
        This assertion method MUST be used in api 'getAccessLog', and param expected_value MUST be an event dict.
        """
        self._step_context.validators.append(
            {"reports_match": [jmes_path, expected_value, message]}
        )
        return self

    def assert_list_sorted_in(
        self,
        jmes_path: Text,
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
            {"sort_list": [jmes_path, expected_value, message]}
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
        self._step_context.extract = {}
        return self

    def with_jmespath(self, jmes_path: Text, var_name: Text) -> "StepRequestExtraction":
        self._step_context.extract[var_name] = jmes_path
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
        self, req_json_update: Union[dict, str], deep=True
    ) -> "RequestWithOptionalArgs":
        """
        Update request.req_json.

        If 'deep' is True, update recursively.

        Note:
            1. if 'with_json()' has not been called, calling this method will set 'request.req_json' directly
                to the value of argument 'update_data'
            2. if 'with_json()' was called before calling this method,
                this method can only be used when json set by 'with_json()' is a json object,
                and json set by 'with_json()' will be updated
            3. if 'with_json()' was called after this method, 'request.req_json' will be overwritten by
                the argument of 'with_json()'. In particular, this method takes no effect.
        """
        self._step_context.request.req_json_update = req_json_update
        self._step_context.request.is_req_json_update_deep = deep

        return self

    def update_form_data(self, data_update: Union[dict, str], deep=True) -> "RequestWithOptionalArgs":
        """
        Update 'request.data' if 'request.data' is a JSON object.

        Note:
            1. if 'with_data()' has not been called, calling this method will set 'request.data' directly
                to the value of argument 'update_data'
            2. if 'with_data()' was called before calling this method,
                this method can only be used when data set by 'with_data()' is a json object,
                and json set by 'with_data()' will be updated
            3. if 'with_data()' was called after this method, 'request.data' will be overwritten by
                the argument of 'with_data()'. In particular, this method takes no effect.
        """
        self._step_context.request.data_update = data_update
        self._step_context.request.is_data_update_deep = deep

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

    def retry_on_failure(
        self, retry_times: int, retry_interval: Union[int, float]
    ) -> "RunRequestSetupMixin":
        """
        Retry request step until success or max retried times.

        :param retry_times: indicate max retried times
        :param retry_interval: sleep between each retry, unit: seconds
        """
        self._step_context.retry_times = retry_times
        self._step_context.max_retry_times = retry_times
        self._step_context.retry_interval = retry_interval
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

    def __init__(self, name: Text = None):  # noqa
        # make sure type of class attributes correct
        if not isinstance(self.config, RequestConfig):
            raise ValueError("type of request config must be RequestConfig")

        # make sure TStep.request exist and is not None
        if not isinstance(
            self.request,
            (RequestWithOptionalArgs, StepRequestValidation, StepRequestExtraction),
        ):
            raise ValueError(
                "type of request must be one of "
                "RequestWithOptionalArgs, StepRequestValidation, or StepRequestExtraction"
            )

        # refer to the duplicate of class attribute 'request' as the default TStep
        # note: copy() is required for class attribute are shared among instances
        step = self.request.perform().copy(deep=True)  # type: TStep

        # move variables from step.variables to step.builtin_variables
        step.builtin_variables = step.variables
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
        return self._step_context
