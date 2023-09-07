import inspect
import json
import os
import time
import uuid
from datetime import datetime
from typing import List, Dict, Text, NoReturn, Union, Callable

from httprunner.builtin import expand_nested_json, update_dict_recursively
from httprunner.configs.emoji import emojis
from httprunner.configs.validation import validation_settings
from httprunner.json_encoders import AllureJSONAttachmentEncoder
from httprunner.pyproject import PyProjectToml

try:
    import allure

    USE_ALLURE = True
except ModuleNotFoundError:
    USE_ALLURE = False

from loguru import logger

from httprunner import utils, exceptions
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
    SessionData,
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

    def __add_allure_attachments(
        self,
        session_data: SessionData,
        validation_results: dict,
        exported_vars: dict,
    ) -> NoReturn:
        """
        Add attachments to allure.
        """
        # split session data into request, response, validation results, export vars, and stat
        # if only one request exists
        if len(session_data.req_resps) == 1:
            request_data = session_data.req_resps[0].request
            response_data = session_data.req_resps[0].response

            # save request data
            if request_at := request_data.headers.get("Date", None):
                request_attachment_name = f"request 🕒 {request_at}"
            else:
                request_attachment_name = "request"
            allure.attach(
                request_data.json(indent=4, ensure_ascii=False),
                request_attachment_name,
                allure.attachment_type.JSON,
            )

            # save response data
            allure.attach(
                response_data.json(indent=4, ensure_ascii=False),
                "response",
                allure.attachment_type.JSON,
            )

            # save validation results
            for validation_result in validation_results.get(
                "validate_extractor", []
            ):  # type: dict
                jmespath_ = validation_result.get(
                    validation_settings.content.keys.jmespath_
                )
                # it is possible that jmespath is not str
                jmespath_ = jmespath_ if isinstance(jmespath_, str) else "NA"

                result = validation_result.pop(
                    validation_settings.content.keys.result, "NA"
                )
                comparator = validation_result.get(
                    validation_settings.content.keys.assert_, {}
                ).get(validation_settings.content.keys.comparator, "NA")

                validation_attachment_name = (
                    f"{result} validate - {jmespath_} / {comparator}"
                )

                allure.attach(
                    json.dumps(
                        validation_result,
                        indent=4,
                        ensure_ascii=False,
                        cls=AllureJSONAttachmentEncoder,
                    ),
                    validation_attachment_name,
                    allure.attachment_type.JSON,
                )

            # save export vars
            allure.attach(
                json.dumps(
                    exported_vars,
                    indent=4,
                    ensure_ascii=False,
                    cls=AllureJSONAttachmentEncoder,
                ),
                "exported variables",
                allure.attachment_type.JSON,
            )

            # save stat
            allure.attach(
                session_data.stat.json(indent=4, ensure_ascii=False),
                "statistics",
                allure.attachment_type.JSON,
            )
        else:
            # put request, response, and validation results in one attachment
            allure.attach(
                self.__session.data.json(indent=4, ensure_ascii=False),
                "session data",
                allure.attachment_type.JSON,
            )
            # save export vars
            allure.attach(
                json.dumps(
                    exported_vars,
                    indent=4,
                    ensure_ascii=False,
                    cls=AllureJSONAttachmentEncoder,
                ),
                "exported variables",
                allure.attachment_type.JSON,
            )

    def __save_allure_data(
        self,
        validation_results: dict,
        exported_vars: dict,
        max_retry_times: int,
        remaining_retry_times: int,
        is_success: bool,
        is_meet_stop_retry_condition: bool = False,
    ) -> NoReturn:
        """
        Save session data as allure raw data after validation completed.

        Note:
            1. this function is exclusively used for method self.__run_step_request().
            2. if retry is needed (max_retries > 0), add new allure step as context
        """
        if not hasattr(self.__session, "data"):
            return

        if max_retry_times > 0:
            if is_success:
                result = emojis.success
            else:
                result = emojis.failure

            if max_retry_times == remaining_retry_times:
                title = f"first request {result}"
            elif remaining_retry_times == 0:
                title = f"retry: {max_retry_times} - last retry {result}"
            else:
                title = f"retry: {max_retry_times - remaining_retry_times} {result}"

            if is_meet_stop_retry_condition:
                title += " (the condition to stop retrying was met)"

            with allure.step(title):
                self.__add_allure_attachments(
                    self.__session.data, validation_results, exported_vars
                )
        else:
            self.__add_allure_attachments(
                self.__session.data, validation_results, exported_vars
            )

    @staticmethod
    def __handle_update_json_object(parsed_request_dict: dict) -> NoReturn:
        """
        Update request with data from update_json_object.
        """
        # skip if `req_json_update` is empty
        if not (req_json_update := parsed_request_dict.pop("req_json_update", None)):
            return

        req_json = parsed_request_dict["req_json"]

        if not isinstance(req_json, dict):
            raise ValueError(
                f"method `update_json_object()` can only be used when `req_json` (after parsing) is a dict, "
                f"but got: {type(req_json)}"
            )

        for update_data, is_deep in req_json_update:
            if not isinstance(update_data, dict):
                raise ValueError(
                    f"the parsed value of argument `req_json_update` in method `update_json_object()` must a dict, "
                    f"but got: {type(req_json)}"
                )
            if is_deep:
                update_dict_recursively(req_json, update_data)
            else:
                req_json.update(update_data)

    @staticmethod
    def __handle_update_form_data(parsed_request_dict: dict) -> NoReturn:
        """
        Update request with data from update_form_data.
        """
        if not (data_update := parsed_request_dict.pop("data_update", None)):
            return

        init_data = parsed_request_dict["data"]

        if not isinstance(init_data, dict):
            raise ValueError(
                f"method `update_form_data()` can only be used when `data` is a dict, "
                f"but got: {type(init_data)}"
            )

        for data_, is_deep in data_update:
            if not isinstance(data_, dict):
                raise ValueError(
                    f"the parsed value of argument `data_update` in method `update_json_object()` must a dict, "
                    f"but got: {type(data_)}"
                )
            if is_deep:
                update_dict_recursively(init_data, data_)
            else:
                init_data.update(data_)

    def __run_step_request(self, step: TStep) -> StepData:
        """run teststep: request"""
        step_data = StepData(name=step.name)

        # parse
        prepare_upload_step(step, self.__project_meta.functions)
        request_dict = step.request.dict()
        request_dict.pop("upload", None)
        parsed_request_dict = parse_data(
            request_dict, step.variables, self.__project_meta.functions
        )

        self.__handle_update_json_object(parsed_request_dict)
        self.__handle_update_form_data(parsed_request_dict)

        parsed_request_dict["headers"].setdefault(
            "HRUN-Request-ID",
            f"HRUN-{self.__case_id}-{str(int(time.time() * 1000))[-6:]}",
        )

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

        # request
        resp = self.__session.request(method, url, **parsed_request_dict)
        resp_obj = ResponseObject(resp)

        # expand nested json if headers contain 'X-Json-Control' and its value is 'expand'
        if parsed_request_dict["headers"].get("X-Json-Control") == "expand":
            expand_nested_json(resp_obj.body)

        step.variables["response"] = resp_obj

        # teardown hooks
        if step.teardown_hooks:
            self.__call_hooks(step.teardown_hooks, step.variables, "teardown request")

        def log_req_resp_details():
            err_msg = "\n{} DETAILED REQUEST & RESPONSE {}\n".format("*" * 32, "*" * 32)

            # log request
            err_msg += "====== request details ======\n"
            err_msg += f"url: {url}\n"
            err_msg += f"method: {method}\n"
            headers = parsed_request_dict.pop("headers", {})
            err_msg += f"headers: {headers}\n"
            for k, v in parsed_request_dict.items():
                v = utils.omit_long_data(v)
                err_msg += f"{k}: {repr(v)}\n"

            err_msg += "\n"

            # log response
            err_msg += "====== response details ======\n"
            err_msg += f"status_code: {resp.status_code}\n"
            err_msg += f"headers: {resp.headers}\n"
            err_msg += f"body: {repr(resp.text)}\n"
            logger.error(err_msg)

        # extract
        extractors: list = step.extract

        # parse JMESPath
        # note: do not change variable 'extractors' directly to reduce surprise
        parsed_extractors = []
        for extractor in extractors:  # type: Union[JMESPathExtractor]
            if isinstance(extractor, JMESPathExtractor):
                if "$" in extractor.expression:
                    extractor = extractor.copy(deep=True)
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

            # cannot export variables extracted
            if local_var_name in extract_mapping:
                raise ValueError(
                    f"cannot export variable {local_var_name} which is extracted from response"
                )

            if local_var_name not in variables_mapping:
                raise ValueError(
                    f"failed to export local step variable {local_var_name}, "
                    f"all step variables now: {variables_mapping}"
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
            self.__session.data.validators = resp_obj.validation_results
            self.__session.data.success = True  # validate success

            if self.__use_allure:
                self.__save_allure_data(
                    resp_obj.validation_results,
                    step_data.export_vars,
                    step.max_retry_times,
                    step.retry_times,
                    self.__session.data.success,
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
                self.__save_allure_data(
                    resp_obj.validation_results,
                    step_data.export_vars,
                    step.max_retry_times,
                    step.retry_times,
                    self.__session.data.success,
                    is_meet_stop_retry_condition,
                )
            self.__session.data.validators = resp_obj.validation_results

            # check if retry is needed
            if step.retry_times > 0 and not is_meet_stop_retry_condition:
                logger.warning(
                    f"step '{step.name}' validation failed, wait {step.retry_interval} seconds and try again"
                )
                step.retry_times -= 1
                time.sleep(step.retry_interval)
                step_data = self.__run_step_request(step)
                return step_data

            self.__failed_steps.append(step)
            log_req_resp_details()

            # log testcase duration before raise ValidationFailure
            self.__duration = time.time() - self.__start_at

            if self.__continue_on_failure:
                self.__session.data.exception = vf
            else:
                raise
        except Exception:
            if self.__use_allure:
                self.__save_allure_data(
                    resp_obj.validation_results,
                    step_data.export_vars,
                    step.max_retry_times,
                    step.retry_times,
                    self.__session.data.success,
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
                f"Invalid teststep referenced testcase: {step.dict()}"
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

    def __run_step(self, step: TStep) -> Dict:
        """run teststep, teststep maybe a request or referenced testcase"""
        is_skip_step = False
        logger.info(f"run step begin: {step.name} >>>>>>")
        step_data = StepData(name=step.name)

        # handle skip_if
        if step.skip_on_condition is not None:
            parsed_skip_condition = parse_data(
                step.skip_on_condition, step.variables, self.__project_meta.functions
            )
            logger.debug(
                f"parsed skip condition: {parsed_skip_condition} ({type(parsed_skip_condition)})"
            )

            # call `eval()` if type is str
            if isinstance(parsed_skip_condition, str):
                parsed_skip_condition = eval(parsed_skip_condition)

            if parsed_skip_condition:
                is_skip_step = True
                parsed_skip_reason = parse_data(
                    step.skip_reason, step.variables, self.__project_meta.functions
                )
                logger.info(f"skip condition was met, reason: {parsed_skip_reason}")

                # mark skipped step as success
                step_data.success = True
            else:
                logger.info("skip condition was not met, run the step")

        # handle skip_unless
        if step.run_on_condition is not None:
            parsed_run_condition = parse_data(
                step.run_on_condition, step.variables, self.__project_meta.functions
            )
            logger.debug(
                f"parsed run condition: {parsed_run_condition} ({type(parsed_run_condition)})"
            )

            # eval again if type is str
            if isinstance(parsed_run_condition, str):
                parsed_run_condition = eval(parsed_run_condition)

            if not parsed_run_condition:
                is_skip_step = True
                parsed_skip_reason = parse_data(
                    step.skip_reason, step.variables, self.__project_meta.functions
                )
                logger.info(f"skip condition was met, reason: {parsed_skip_reason}")

                # mark skipped step as success
                step_data.success = True
            else:
                logger.info("run condition was met, run the step")

        if not is_skip_step:
            if step.request:
                step_data = self.__run_step_request(step)
            elif step.testcase:
                step_data = self.__run_step_testcase(step)
            else:
                raise ParamsError(
                    f"teststep is neither a request nor a referenced testcase: {step.dict()}"
                )

        self.__step_datas.append(step_data)
        logger.info(f"run step end: {step.name} <<<<<<\n")
        return step_data.export_vars

    def __parse_config(self, config: TConfig) -> NoReturn:
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

    def __parse_validate_parametrized_step_parameters(self, step: TStep) -> NoReturn:
        """Parse and validate parameters of specific parametrized step."""
        argnames, argvalues, ids = step.parametrize

        # make sure argnames is a str
        if not isinstance(argnames, str):
            raise TypeError(
                f"type of argnames must be str, but got {type(argnames)}\n"
                f"Hint: use comma to split multiple arguments"
            )

        argvalues = parse_data(argvalues, step.variables, self.__project_meta.functions)
        ids = parse_data(ids, step.variables, self.__project_meta.functions)

        if not isinstance(argvalues, (list, tuple)):
            raise TypeError(
                f"type of argvalues after parsing must be either list or tuple, but got {type(argvalues)}"
            )

        if not argvalues:
            raise ValueError("argvalues cannot be an empty list")

        if "," in argnames:
            argnames = [_.strip() for _ in argnames.split(",")]

            # each element should be a tuple
            for argvalue in argvalues:
                if not isinstance(argvalue, (tuple, list)):
                    raise TypeError(
                        "type of each argvalue-element must be tuple or list if argnames contain comma"
                    )

                if len(argvalue) != len(argnames):
                    raise ValueError(
                        "length of each argvalue-element must be equal to argnames if argnames contain comma"
                    )

        if ids is not None:
            if not isinstance(ids, (list, tuple)):
                raise TypeError(
                    f"if ids was specified, it's type must be list or tuple, but got {type(ids)}"
                )

            if len(ids) != len(argvalues):
                raise ValueError(
                    "length of ids must be equal to parsed argvalues if ids is a list or tuple"
                )

        step.parametrize = (argnames, argvalues, ids)

    def __expand_parametrized_step(self, origin_step: TStep) -> list[TStep]:
        """
        Expand one parametrized step.

        :param origin_step: the original step to be expanded
        """
        self.__parse_validate_parametrized_step_parameters(origin_step)

        # argnames, argvalues, and ids have already been parsed
        argnames, argvalues, ids = origin_step.parametrize

        # eliminate 'parametrize' to avoid expanding this step again
        origin_step.parametrize = None

        expanded_steps = []
        for i, argvalue in enumerate(argvalues):
            # convert arguments to step variables
            if isinstance(argnames, list):
                variables = dict(zip(argnames, argvalue))
            else:
                variables = {argnames: argvalue}

            # deep copy step
            expanded_step = origin_step.copy(deep=True)

            # parametrize variables > step.with_variables
            expanded_step.variables.update(variables)

            # determine id
            id = i + 1
            if ids:
                if isinstance(ids, (list, tuple)):
                    id = ids[i]
                # Note: ids as Callable is not supported yet
                elif isinstance(ids, Callable):
                    id = ids()

            # append id to step name
            expanded_step.name += f" - {id}"

            expanded_steps.append(expanded_step)

        return expanded_steps

    def __run_steps(self, steps: list[TStep], extracted_variables: dict) -> NoReturn:
        """Iterate and run steps."""
        for step in steps:
            # variables got from outside of step
            # extracted variables > testcase config variables
            step_config_variables = merge_variables(
                extracted_variables, self.__config.variables
            )

            # step variables set with HttpRunnerRequest.with_variables() > step outside variables
            step.variables = merge_variables(step.variables, step_config_variables)

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

            if step.parametrize:
                # step.variables have already been parsed
                expanded_steps = self.__expand_parametrized_step(step)
                self.__run_steps(expanded_steps, extracted_variables)
                continue

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

            # parse step name for allure report
            step.name = parse_data(
                step.name, step.variables, self.__project_meta.functions
            )

            # run step
            try:
                if self.__use_allure:
                    with allure.step(f"step: {step.name}"):
                        extract_mapping = self.__run_step(step)

                        # raise exception to mark this step failed in allure report
                        # run only when self.__continue_on_failure is True
                        if not (step_data := self.__step_datas[-1]).success:
                            if step.request:
                                raise step_data.data.exception
                            else:
                                raise ValidationFailure(
                                    "self.__continue_on_failure is set to True and step.testcase failed"
                                )
                else:
                    extract_mapping = self.__run_step(step)

                    if not (step_data := self.__step_datas[-1]).success:
                        if step.request:
                            raise step_data.data.exception
                        else:
                            raise ValidationFailure(
                                "self.__continue_on_failure is set to True and step.testcase failed"
                            )
            except ValidationFailure:
                if not self.__continue_on_failure:
                    raise

            extracted_variables.update(extract_mapping)

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
        # save extracted variables of teststeps
        extracted_variables: VariablesMapping = {}

        self.__run_steps(self.__teststeps, extracted_variables)

        # save extracted variables to session variables
        self.__session_variables.update(extracted_variables)
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
        self.__case_id = self.__case_id or str(uuid.uuid4())
        self.__log_path = self.__log_path or os.path.join(
            self.__project_meta.httprunner_root_path,
            "logs",
            f"{self.__case_id}.run.log",
        )
        # do not save logging messages to log files to free disk space
        # log_handler = logger.add(self.__log_path, level="DEBUG")

        # parse config name
        config_variables = self.__config.variables
        if args:
            config_variables.update(args[0])
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

        try:
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
        finally:
            pass
            # logger.remove(log_handler)
            # logger.info(f"generate testcase log: {self.__log_path}")
