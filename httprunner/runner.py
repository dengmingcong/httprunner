import inspect
import os
import time
from copy import deepcopy
from datetime import datetime
from typing import List, Dict, Text, NoReturn, Union

from httprunner.builtin import expand_nested_json
from httprunner.core.allure.runrequest.runrequest_retry import save_run_request_retry
from httprunner.core.runner.parametrized_step import expand_parametrized_step
from httprunner.core.runner.skip_step import is_skip_step
from httprunner.core.runner.update_form import update_form
from httprunner.core.runner.update_json import update_json
from httprunner.pyproject import PyProjectToml

try:
    import allure

    USE_ALLURE = True
except ModuleNotFoundError:
    USE_ALLURE = False

from loguru import logger

from httprunner import exceptions
from httprunner.client import HttpSession
from httprunner.exceptions import ValidationFailure, ParamsError, VariableNotFound
from httprunner.ext.uploader import prepare_upload_step
from httprunner.loader import load_project_meta, load_testcase_file
from httprunner.parser import (
    build_url,
    parse_data,
    parse_variables_mapping,
    update_url_origin,
)
from httprunner.response import ResponseObject
from httprunner.testcase import Config, Step
from httprunner.utils import merge_variables
from httprunner.models import (
    TConfig,
    TStep,
    VariablesMapping,
    StepData,
    TestCaseSummary,
    TestCaseTime,
    TestCaseInOut,
    ProjectMeta,
    TestCase,
    Hooks,
    StepExport,
    ConfigExport,
    JMESPathExtractor,
)


class HttpRunner(object):
    config: Config
    teststeps: List[Step]

    success: bool = False  # indicate testcase execution result
    __config: TConfig
    __teststeps: List[TStep]
    __project_meta: ProjectMeta = None
    __case_id: Text = ""
    __export: Union[StepExport, ConfigExport] = None  # testcase export
    __step_datas: List[StepData] = []
    __session: HttpSession = None

    # only variables in __session_variables can be exported,
    # __session_variables will be set to step variables when running testcase step
    __session_variables: VariablesMapping = {}
    # time
    __start_at: float = 0
    __duration: float = 0
    # log
    __log_path: Text = ""
    __continue_on_failure: bool = False
    __use_allure: bool = USE_ALLURE

    def __init_subclass__(cls):
        """Add validation for subclass."""
        super().__init_subclass__()

        # make sure type of attribute 'config' correct
        if not isinstance(cls.config, Config):
            raise TypeError(
                f"type of class attribute 'config' must be Config, but got {type(cls.config)}"
            )

        # make sure teststeps is a list
        if not isinstance(cls.teststeps, list):
            raise TypeError(
                f"type of class attribute 'teststeps' must be list, but got {type(cls.teststeps)}"
            )

        for step in cls.teststeps:
            # make sure every element of teststeps is a Step instance
            if not isinstance(step, Step):
                raise TypeError(
                    f"type of each test step must be Step, but got {type(step)}"
                )

        # update config.path
        cls.config.path = inspect.getfile(cls)

    def __init_tests__(self) -> NoReturn:
        self.__config = self.config.perform()
        self.__teststeps = []
        for step in self.teststeps:
            self.__teststeps.append(step.perform())
        self.__failed_steps: list[TStep] = []

    def set_use_allure(self, is_use_allure: bool) -> "HttpRunner":
        """
        set if saving allure data no matter if allure was installed
        """
        self.__use_allure = is_use_allure
        return self

    @property
    def raw_testcase(self) -> TestCase:
        if not hasattr(self, "__config"):
            self.__init_tests__()

        return TestCase(config=self.__config, teststeps=self.__teststeps)

    def with_project_meta(self, project_meta: ProjectMeta) -> "HttpRunner":
        self.__project_meta = project_meta
        return self

    def with_session(self, session: HttpSession) -> "HttpRunner":
        self.__session = session
        return self

    def with_case_id(self, case_id: Text) -> "HttpRunner":
        self.__case_id = case_id
        return self

    def with_variables(self, variables: VariablesMapping) -> "HttpRunner":
        self.__session_variables = variables
        return self

    def set_continue_on_failure(self, is_continue_on_failure: bool) -> "HttpRunner":
        self.__continue_on_failure = is_continue_on_failure
        return self

    def with_export(self, step_export: StepExport) -> "HttpRunner":
        self.__export = step_export
        return self

    def __call_hooks(
        self,
        hooks: Hooks,
        step_variables: VariablesMapping,
        hook_msg: Text,
    ) -> NoReturn:
        """call hook actions.

        Args:
            hooks (list): each hook in hooks list maybe in two format.

                format1 (str): only call hook functions.
                    ${func()}
                format2 (dict): assignment, the value returned by hook function will be assigned to variable.
                    {"var": "${func()}"}

            step_variables: current step variables to call hook, include two special variables

                request: parsed request dict
                response: ResponseObject for current response

            hook_msg: setup/teardown request/testcase

        """
        logger.info(f"call hook actions: {hook_msg}")

        if not isinstance(hooks, List):
            logger.error(f"Invalid hooks format: {hooks}")
            return

        for hook in hooks:
            if isinstance(hook, Text):
                # format 1: ["${func()}"]
                logger.debug(f"call hook function: {hook}")
                parse_data(hook, step_variables, self.__project_meta.functions)
            elif isinstance(hook, Dict) and len(hook) == 1:
                # format 2: {"var": "${func()}"}
                var_name, hook_content = list(hook.items())[0]
                hook_content_eval = parse_data(
                    hook_content, step_variables, self.__project_meta.functions
                )
                logger.debug(
                    f"call hook function: {hook_content}, got value: {hook_content_eval}"
                )
                logger.debug(f"assign variable: {var_name} = {hook_content_eval}")
                step_variables[var_name] = hook_content_eval
            else:
                logger.error(f"Invalid hook format: {hook}")

    def __prepare_step_request(self, step: TStep) -> tuple:
        """Prepare before sending http request."""
        # parse
        prepare_upload_step(step, self.__project_meta.functions)

        # fix: filehandler will be converted to SerializationIterator and file content will be lost.
        # dict(model) will return raw field values and avoid SerializationIterator.
        # refer: https://docs.pydantic.dev/2.5/concepts/serialization/#dictmodel-and-iteration
        request_dict = dict(step.request)
        request_dict.pop("upload", None)
        parsed_request_dict = parse_data(
            request_dict, step.variables, self.__project_meta.functions
        )

        update_json(parsed_request_dict)
        update_form(parsed_request_dict)

        # add http headers for every http request
        try:
            parsed_request_dict["headers"].update(PyProjectToml().http_headers)
        except KeyError:
            logger.debug("no extra http headers in pyproject.toml")

        step.variables["request"] = parsed_request_dict
        step.variables["session"] = self.__session

        # setup hooks
        if step.setup_hooks:
            self.__call_hooks(step.setup_hooks, step.variables, "setup request")

        # prepare arguments
        method = parsed_request_dict.pop("method")
        url_path = parsed_request_dict.pop("url")
        url = build_url(self.__config.base_url, url_path)

        # substitute origin if request.origin is not None
        if origin := parsed_request_dict.pop("origin"):
            url = update_url_origin(url, origin)

        parsed_request_dict["verify"] = self.__config.verify
        parsed_request_dict["json"] = parsed_request_dict.pop("req_json", {})

        return method, url, parsed_request_dict

    def __run_step_request(self, step: TStep) -> StepData:
        """run teststep: request"""
        step_data = StepData(name=step.name)

        method, url, parsed_request_dict = self.__prepare_step_request(step)

        # request
        resp = self.__session.request(method, url, **parsed_request_dict)
        resp_obj = ResponseObject(resp)

        # expand nested json if headers contain 'X-Json-Control' and its value is 'expand'.
        # Note: The header is case-sensitive.
        if parsed_request_dict["headers"].get("X-Json-Control") == "expand":
            expand_nested_json(resp_obj.body)

        step.variables["response"] = resp_obj

        # teardown hooks
        if step.teardown_hooks:
            self.__call_hooks(step.teardown_hooks, step.variables, "teardown request")

        # extract
        extractors: list = step.extract

        # parse JMESPath
        # note: do not change variable 'extractors' directly to reduce surprise
        parsed_extractors = []
        for extractor in extractors:  # type: Union[JMESPathExtractor]
            if isinstance(extractor, JMESPathExtractor):
                if "$" in extractor.expression:
                    extractor = extractor.model_copy(deep=True)
                    extractor.expression = parse_data(
                        extractor.expression,
                        step.variables,
                        self.__project_meta.functions,
                    )
                parsed_extractors.append(extractor)

        extract_mapping = resp_obj.extract(parsed_extractors)
        step_data.export_vars = extract_mapping

        variables_mapping = step.variables
        variables_mapping.update(extract_mapping)

        # added by @deng at 2022.2.9
        export_mapping = {}
        # export local variables to make them usable for steps next
        for var in step.globalize:
            if isinstance(var, dict):
                if len(var) != 1:
                    raise ValueError(
                        f"length of dict can only be 1 but got {len(var)} for: {var}"
                    )
                local_var_name = list(var.keys())[0]
                export_as = list(var.values())[0]
            else:
                if not isinstance(var, str) or not var:
                    raise ValueError(
                        "type of var can only be dict or str, and must not be empty"
                    )
                local_var_name = var
                export_as = var

            if local_var_name not in variables_mapping:
                raise ValueError(
                    f"failed to export local step variable {local_var_name}, "
                    f"all step variables now: {variables_mapping.keys()}"
                )

            export_mapping[export_as] = variables_mapping[local_var_name]

        # extracted variables > local variables
        step_data.export_vars = merge_variables(step_data.export_vars, export_mapping)

        # validate
        validators = step.validators
        self.__session.data.success = (
            False  # default to False, re-assign it to make it more explicit
        )

        try:
            resp_obj.validate(
                validators, variables_mapping, self.__project_meta.functions
            )
            self.__session.data.validation_results = resp_obj.validation_results
            self.__session.data.success = True  # validate success

            if self.__use_allure:
                save_run_request_retry(
                    self.__session,
                    resp_obj,
                    step_data.export_vars,
                    step.max_retry_times,
                    step.remaining_retry_times,
                )
        except ValidationFailure as vf:
            # evaluate `stop_retry_if` before retrying
            is_meet_stop_retry_condition = False
            if step.stop_retry_if is not None:
                parsed_stop_retry_if = parse_data(
                    step.stop_retry_if, step.variables, self.__project_meta.functions
                )
                logger.debug(f"parsed `stop_retry_if`: {parsed_stop_retry_if}")

                # call `eval()` if type is str
                if isinstance(parsed_stop_retry_if, str):
                    parsed_stop_retry_if = eval(parsed_stop_retry_if)

                if parsed_stop_retry_if:
                    is_meet_stop_retry_condition = True
                    logger.info(
                        "`stop_retry_if` condition was met, retrying was stopped"
                    )

            if self.__use_allure:
                save_run_request_retry(
                    self.__session,
                    resp_obj,
                    step_data.export_vars,
                    step.max_retry_times,
                    step.remaining_retry_times,
                    is_meet_stop_retry_condition,
                )
            self.__session.data.validation_results = resp_obj.validation_results

            # check if retry is needed
            if step.remaining_retry_times > 0 and not is_meet_stop_retry_condition:
                logger.warning(
                    f"step '{step.name}' validation failed, wait {step.retry_interval} seconds and try again"
                )
                step.remaining_retry_times -= 1
                time.sleep(step.retry_interval)
                step_data = self.__run_step_request(step)
                return step_data

            self.__failed_steps.append(step)

            # log testcase duration before raise ValidationFailure
            self.__duration = time.time() - self.__start_at

            if self.__continue_on_failure:
                self.__session.data.exception = vf
            else:
                raise
        except Exception:
            if self.__use_allure:
                save_run_request_retry(
                    self.__session,
                    resp_obj,
                    step_data.export_vars,
                    step.max_retry_times,
                    step.remaining_retry_times,
                )
            raise
        finally:
            if hasattr(self, "__failed_steps") and self.__failed_steps:
                self.success = False
            else:
                self.success = True

            step_data.success = self.__session.data.success

            if hasattr(self.__session, "data"):
                # httprunner.client.HttpSession, not locust.clients.HttpSession
                # save step data
                step_data.data = self.__session.data

        return step_data

    def __run_step_testcase(self, step: TStep) -> StepData:
        """run teststep: referenced testcase"""
        step_data = StepData(name=step.name)
        step_variables = step.variables
        step_export = step.export

        # setup hooks
        if step.setup_hooks:
            self.__call_hooks(step.setup_hooks, step_variables, "setup testcase")

        if hasattr(step.testcase, "config") and hasattr(step.testcase, "teststeps"):
            testcase_cls = step.testcase
            case_result = (
                testcase_cls()
                .set_continue_on_failure(self.__continue_on_failure)
                .set_use_allure(self.__use_allure)
                .with_session(self.__session)
                .with_case_id(self.__case_id)
                .with_variables(step_variables)
                .with_export(step_export)
                .run()
            )

        elif isinstance(step.testcase, Text):
            if os.path.isabs(step.testcase):
                ref_testcase_path = step.testcase
            else:
                ref_testcase_path = os.path.join(
                    self.__project_meta.httprunner_root_path, step.testcase
                )

            case_result = (
                HttpRunner()
                .set_continue_on_failure(self.__continue_on_failure)
                .set_use_allure(self.__use_allure)
                .with_session(self.__session)
                .with_case_id(self.__case_id)
                .with_variables(step_variables)
                .with_export(step_export)
                .run_path(ref_testcase_path)
            )

        else:
            raise exceptions.ParamsError(
                f"Invalid teststep referenced testcase: {step.model_dump()}"
            )

        # teardown hooks
        if step.teardown_hooks:
            self.__call_hooks(step.teardown_hooks, step.variables, "teardown testcase")

        step_data.data = case_result.get_step_datas()  # list of step data
        step_data.export_vars = case_result.get_export_variables()

        if case_result.get_failed_steps():
            step_data.success = False
            self.__failed_steps.append(step)
        else:
            step_data.success = True

        if self.__failed_steps:
            self.success = False
        else:
            self.success = True

        if step_data.export_vars:
            logger.info(f"export variables: {step_data.export_vars}")

        return step_data

    def __resolve_step_variables(
        self, step: TStep, step_context_variables: dict
    ) -> NoReturn:
        """Parse step variables with step context variables and variables defined by step self."""
        # step variables set with HttpRunnerRequest.with_variables() > step outside variables
        step.variables = merge_variables(step.variables, step_context_variables)

        # parse variables
        step.variables = parse_variables_mapping(
            step.variables, self.__project_meta.functions
        )

        # parse raw variables
        if step.raw_variables:
            parsed_raw_variables = parse_data(
                step.raw_variables, step.variables, self.__project_meta.functions
            )
            if step.is_deep_parse_raw_variables:
                parsed_raw_variables = parse_data(
                    parsed_raw_variables,
                    step.variables,
                    self.__project_meta.functions,
                )
            step.variables.update(parsed_raw_variables)

        # for HttpRunnerRequest step
        if step.request_config:
            # step variables set with HttpRunnerRequest.with_variables() >
            # extracted variables > testcase config variables > HttpRunnerRequest config variables
            step.variables = merge_variables(
                step.variables, step.request_config.variables
            )

            # step config variables are supposed to be self-parsed before merged into step.variables
            step.variables = parse_variables_mapping(
                step.variables, self.__project_meta.functions
            )

            # final priority order:
            # step private variables > step variables set with HttpRunnerRequest.with_variables() >
            # extracted variables > testcase config variables > HttpRunnerRequest config variables
            step.variables = merge_variables(step.private_variables, step.variables)

            # parse variables
            step.variables = parse_variables_mapping(
                step.variables, self.__project_meta.functions
            )

    def __display_skipped_step(
        self, step: TStep, step_context_variables: dict
    ) -> NoReturn:
        """Generate allure report for skipped step."""
        step_data = StepData(name=step.name)
        # mark skipped step as success
        step_data.success = True
        try:
            step.name = parse_data(
                step.name, step_context_variables, self.__project_meta.functions
            )
        except VariableNotFound as e:
            logger.warning(f"error occurred while parsing step name: {repr(e)}")

        with allure.step(step.name):
            self.__step_datas.append(step_data)

    def __run_step(self, step: TStep, step_context_variables: dict) -> NoReturn:
        """run teststep, teststep maybe a request or referenced testcase"""
        # expand and run parametrized steps
        if step.parametrize:
            expanded_steps = expand_parametrized_step(
                step, step_context_variables, self.__project_meta.functions
            )
            self.__run_steps(expanded_steps, step_context_variables)

            # important: parametrized step is a step wrapper, codes later was not needed for itself
            return

        # parsed parametrize variables > extracted variables > testcase config variables.
        # Note: parsed parametrize variables will be used in skip_if and skip_unless condition
        step_context_variables.update(step.parsed_parametrize_vars)

        # skip step if condition is satisfied
        if is_skip_step(step, step_context_variables, self.__project_meta.functions):
            self.__display_skipped_step(step, step_context_variables)
            # important: return directly if step is skipped
            return

        self.__resolve_step_variables(step, step_context_variables)

        # parse step name for allure report
        try:
            step.name = parse_data(
                step.name, step.variables, self.__project_meta.functions
            )
        except VariableNotFound as e:
            logger.warning(f"error occurred while parsing step name: {repr(e)}")

        logger.info(f"run step begin: {step.name} >>>>>>")

        def step_runner(step_: TStep) -> StepData:
            """Run step."""
            if step.request:
                return self.__run_step_request(step_)
            elif step.testcase:
                return self.__run_step_testcase(step_)
            else:
                raise ParamsError(
                    f"teststep is neither a request nor a referenced testcase: {step.model_dump()}"
                )

        if self.__use_allure:
            with allure.step(step.name):
                step_data = step_runner(step)
        else:
            step_data = step_runner(step)

        self.__step_datas.append(step_data)
        logger.info(f"run step end: {step.name} <<<<<<\n")

        # update step context variables with new extracted variables
        step_context_variables.update(step_data.export_vars)

        # put extracted variables to session variables for later exporting
        self.__session_variables.update(step_data.export_vars)

    def __parse_config(self, config: TConfig) -> NoReturn:
        """Parse TConfig instance."""
        # session variables > config variables
        config.variables.update(self.__session_variables)
        config.variables = parse_variables_mapping(
            config.variables, self.__project_meta.functions
        )
        config.name = parse_data(
            config.name, config.variables, self.__project_meta.functions
        )
        config.base_url = parse_data(
            config.base_url, config.variables, self.__project_meta.functions
        )

    def __run_steps(self, steps: list[TStep], step_context_variables) -> NoReturn:
        """Iterate and run steps."""
        for step in steps:
            # run step
            self.__run_step(step, step_context_variables)

    def run_testcase(self, testcase: TestCase) -> "HttpRunner":
        """run specified testcase

        Examples:
            testcase_obj = TestCase(config=TConfig(...), teststeps=[TStep(...)])
            HttpRunner().with_project_meta(...).run_testcase(testcase_obj)
        """
        self.__config = testcase.config
        self.__teststeps = testcase.teststeps

        # prepare
        self.__project_meta = self.__project_meta or load_project_meta()
        self.__parse_config(self.__config)

        self.__start_at = time.time()
        self.__step_datas: List[StepData] = []
        self.__session = self.__session or HttpSession()

        # init step context variables as to testcase config variables (already merged session variables)
        step_context_variables = deepcopy(self.__config.variables)
        self.__run_steps(self.__teststeps, step_context_variables)

        self.__duration = time.time() - self.__start_at

        return self

    def run_path(self, path: Text) -> "HttpRunner":
        if not os.path.isfile(path):
            raise exceptions.ParamsError(f"Invalid testcase path: {path}")

        testcase_obj = load_testcase_file(path)
        return self.run_testcase(testcase_obj)

    def run(self) -> "HttpRunner":
        """run current testcase

        Examples:
            TestCaseRequestWithFunctions().run()
        """
        self.__init_tests__()
        testcase_obj = TestCase(config=self.__config, teststeps=self.__teststeps)
        return self.run_testcase(testcase_obj)

    def get_step_datas(self) -> List[StepData]:
        return self.__step_datas

    def validate_testcase_export(self) -> NoReturn:
        """Validate testcase export."""
        if isinstance(self.__export, StepExport):
            same_key_value_items = []
            for var_name, var_alias in self.__export.var_alias_mapping.items():
                # type of var alias must be str
                if not isinstance(var_alias, str):
                    raise ParamsError(
                        f"type of variable alias '{var_alias}' is not str, but got {type(var_alias)}"
                    )

                # var alias must not in var_names, otherwise exported variables will be overwritten
                if var_alias in self.__export.var_names:
                    raise ParamsError(
                        f"variable alias ({var_alias}) must not in var_names {self.__export.var_names}"
                    )

                # handle if var_name equals var_alias
                if var_name == var_alias:
                    self.__export.var_names.append(var_name)
                    same_key_value_items.append(var_name)

            # pop keys (do pop in iteration will cause 'dictionary changed size during iteration' error)
            for var_name in same_key_value_items:
                self.__export.var_alias_mapping.pop(var_name)

            # find non-exist variables
            if non_exist_vars := (
                set(self.__export.var_names).union(
                    set(self.__export.var_alias_mapping.keys())
                )
                - set(self.__session_variables.keys())
            ):
                raise VariableNotFound(
                    f"fail to export variables {non_exist_vars} from session variables"
                )

        elif isinstance(self.__export, list):
            # Make sure variables specified exist in session variables.
            if non_exist_vars := set(self.__export) - set(
                self.__session_variables.keys()
            ):
                raise VariableNotFound(
                    f"fail to export variables {non_exist_vars} from session variables."
                )
        else:
            raise ParamsError(
                f"type of testcase export is supposed to be StepExport or ConfigExport, but got {type(self.__export)}"
            )

    def get_export_variables(self) -> dict:
        """Export variables from testcase referenced."""

        # override testcase export vars with step export
        self.__export = self.__export or self.__config.export
        self.validate_testcase_export()

        export_vars_mapping = {}

        if isinstance(self.__export, StepExport):
            var_names_set = set(self.__export.var_names)
            var_alias_mapping_keys_set = set(self.__export.var_alias_mapping.keys())

            var_names_only_set = var_names_set - var_alias_mapping_keys_set

            # export variable as both var_name and var_alias
            for var_name in var_alias_mapping_keys_set:
                var_alias = self.__export.var_alias_mapping[var_name]
                export_vars_mapping[var_name] = (
                    var_value := self.__session_variables[var_name]
                )
                export_vars_mapping[var_alias] = var_value

            # export variable as var_name only
            for var_name in var_names_only_set:
                export_vars_mapping[var_name] = self.__session_variables[var_name]
        else:
            for var_name in self.__export:
                export_vars_mapping[var_name] = self.__session_variables[var_name]

        return export_vars_mapping

    def get_failed_steps(self) -> List[TStep]:
        """
        Returns failed steps.

        self.__failed_steps is a private attribute and cannot be accessed by instance directly.
        """
        return self.__failed_steps

    def get_summary(self) -> TestCaseSummary:
        """get testcase result summary"""
        start_at_timestamp = self.__start_at
        start_at_iso_format = datetime.utcfromtimestamp(start_at_timestamp).isoformat()
        return TestCaseSummary(
            name=self.__config.name,
            success=self.success,
            case_id=self.__case_id,
            time=TestCaseTime(
                start_at=self.__start_at,
                start_at_iso_format=start_at_iso_format,
                duration=self.__duration,
            ),
            in_out=TestCaseInOut(
                config_vars=self.__config.variables,
                export_vars=self.get_export_variables(),
            ),
            log=self.__log_path,
            step_datas=self.__step_datas,
        )

    def test_start(self, *args: dict, **_ignored) -> "HttpRunner":
        """
        Main entrance for pytest discovering.

        Only the first argument will be used, and it must be a dict.All other arguments will be ignored.
        """
        """
        Why defining the method parameters as `*args: dict, **_ignored` is just to skip this warning:
            > Signature of method 'TestCaseRequestWithVariables.test_start()' does not match
            > signature of the base method in class 'HttpRunner'
        """
        self.__init_tests__()
        self.__continue_on_failure = self.__config.continue_on_failure

        # the location of the first testcase decided the project meta
        # for project meta would usually be located once
        self.__project_meta = self.__project_meta or load_project_meta()

        self.__log_path = self.__log_path or os.path.join(
            self.__project_meta.httprunner_root_path,
            "logs",
            f"{self.__case_id}.run.log",
        )

        # parse config name
        config_variables = self.__config.variables
        if args:
            config_variables.update(args[0])

        # override config variables with session variables, just for parsing config name
        config_variables.update(self.__session_variables)
        self.__config.name = parse_data(
            self.__config.name, config_variables, self.__project_meta.functions
        )

        if self.__use_allure:
            # update allure report meta
            allure.dynamic.title(self.__config.name)
            allure.dynamic.description(type(self).__doc__)

        logger.info(
            f"Start to run testcase: {self.__config.name}, TestCase ID: {self.__case_id}"
        )

        case_result = self.run_testcase(
            TestCase(config=self.__config, teststeps=self.__teststeps)
        )

        # mark testcase as failed finally after all steps were executed and failed steps existed
        if self.__continue_on_failure:
            if self.__failed_steps:
                self.success = False
                raise ValidationFailure(
                    f"continue_on_failure was set to True and {len(self.__failed_steps)} steps failed."
                )
            else:
                self.success = True

        return case_result
