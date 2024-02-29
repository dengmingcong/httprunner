from typing import Dict, Text, Any, NoReturn, Union

import jmespath
import requests
from jmespath.exceptions import JMESPathError
from loguru import logger

from httprunner import exceptions
from httprunner.configs.emoji import emojis
from httprunner.configs.validation import validation_settings
from httprunner.exceptions import ValidationFailure, ParamsError
from httprunner.models import (
    VariablesMapping,
    Validator,
    FunctionsMapping,
    JMESPathExtractor,
)
from httprunner.parser import parse_data, parse_string_value, get_mapping_function
from httprunner.utils import omit_long_data


def get_uniform_comparator(comparator: Text):
    """convert comparator alias to uniform name.

    Note:
        This function is deprecated and will be removed in the future.
    """
    if comparator in ["eq", "equals", "equal"]:
        return "equal"
    elif comparator in ["lt", "less_than"]:
        return "less_than"
    elif comparator in ["le", "less_or_equals"]:
        return "less_or_equals"
    elif comparator in ["gt", "greater_than"]:
        return "greater_than"
    elif comparator in ["ge", "greater_or_equals"]:
        return "greater_or_equals"
    elif comparator in ["ne", "not_equal"]:
        return "not_equal"
    elif comparator in ["str_eq", "string_equals"]:
        return "string_equals"
    elif comparator in ["len_eq", "length_equal"]:
        return "length_equal"
    elif comparator in [
        "len_gt",
        "length_greater_than",
    ]:
        return "length_greater_than"
    elif comparator in [
        "len_ge",
        "length_greater_or_equals",
    ]:
        return "length_greater_or_equals"
    elif comparator in ["len_lt", "length_less_than"]:
        return "length_less_than"
    elif comparator in [
        "len_le",
        "length_less_or_equals",
    ]:
        return "length_less_or_equals"
    else:
        return comparator


def uniform_validator(validator):
    """unify validator

    Note:
        This function is deprecated and will be removed in the future.

    Args:
        validator (dict): validator maybe in two formats:

            format1: this is kept for compatibility with the previous versions.
                {"check": "status_code", "comparator": "eq", "expect": 201}
                {"check": "$resp_body_success", "comparator": "eq", "expect": True}
            format2: recommended new version, {assert: [check_item, expected_value]}
                {'eq': ['status_code', 201]}
                {'eq': ['$resp_body_success', True]}

    Returns
        dict: validator info

            {
                "check": "status_code",
                "expect": 201,
                "assert": "equals"
            }

    """
    if not isinstance(validator, dict):
        raise ParamsError(f"invalid validator: {validator}")

    if "check" in validator and "expect" in validator:
        # format1
        check_item = validator["check"]
        expect_value = validator["expect"]
        message = validator.get("message", "")
        comparator = validator.get("comparator", "eq")

    elif len(validator) == 1:
        # format2
        comparator = list(validator.keys())[0]
        compare_values = validator[comparator]

        if not isinstance(compare_values, list) or len(compare_values) not in [2, 3]:
            raise ParamsError(f"invalid validator: {validator}")

        check_item = compare_values[0]
        expect_value = compare_values[1]
        if len(compare_values) == 3:
            message = compare_values[2]
        else:
            # len(compare_values) == 2
            message = ""

    else:
        raise ParamsError(f"invalid validator: {validator}")

    # uniform comparator, e.g. lt => less_than, eq => equals
    assert_method = get_uniform_comparator(comparator)

    return {
        "check": check_item,
        "expect": expect_value,
        "assert": assert_method,
        "message": message,
    }


class ResponseObject(object):
    def __init__(self, requests_response: requests.Response):
        """initialize with a requests.Response object

        Args:
            requests_response (instance): requests.Response instance

        """
        self.resp_obj = requests_response
        self.validation_results: Dict = {}

    def __getattr__(self, key):
        if key in ["json", "content", "body"]:
            try:
                value = self.resp_obj.json()
            except ValueError:
                value = self.resp_obj.content
        elif key == "cookies":
            value = self.resp_obj.cookies.get_dict()
        else:
            try:
                value = getattr(self.resp_obj, key)
            except AttributeError:
                err_msg = "ResponseObject does not have attribute: {}".format(key)
                logger.error(err_msg)
                raise exceptions.ParamsError(err_msg)

        self.__dict__[key] = value
        return value

    def _search_jmespath(self, expr: Text) -> Any:
        resp_obj_meta = {
            "status_code": self.status_code,
            "headers": self.headers,
            "cookies": self.cookies,
            "body": self.body,
        }
        try:
            check_value = jmespath.search(expr, resp_obj_meta)
        except JMESPathError as ex:
            logger.error(
                f"failed to search with jmespath\n"
                f"expression: {expr}\n"
                f"data: {resp_obj_meta}\n"
                f"exception: {ex}"
            )
            raise

        return check_value

    def extract(self, extractors: list[Union[JMESPathExtractor]]) -> Dict[Text, Any]:
        if not extractors:
            return {}

        extract_mapping = {}
        for extractor in extractors:  # type: Union[JMESPathExtractor]
            if isinstance(extractor, JMESPathExtractor):
                field_value = self._search_jmespath(extractor.expression)

                if extractor.sub_extractor:
                    field_value = extractor.sub_extractor(field_value)

                extract_mapping[extractor.variable_name] = field_value

        logger.info(f"extract mapping: {extract_mapping}")
        return extract_mapping

    def validate(
        self,
        validators: list[Validator],
        variables_mapping: VariablesMapping = None,
        functions_mapping: FunctionsMapping = None,
    ) -> NoReturn:

        variables_mapping = variables_mapping or {}
        functions_mapping = functions_mapping or {}

        self.validation_results = {}
        if not validators:
            return

        validate_pass = True
        failures = []

        for validator in validators:

            if "validate_extractor" not in self.validation_results:
                self.validation_results["validate_extractor"] = []

            # check item (jmespath)
            check_item = validator.expression
            if isinstance(check_item, Text) and "$" in check_item:
                # check_item is variable or function
                check_item = parse_data(
                    check_item, variables_mapping, functions_mapping
                )
                check_item = parse_string_value(check_item)

            if check_item and isinstance(check_item, Text):
                check_value = self._search_jmespath(check_item)  # actual value
            else:
                # variable or function evaluation result is "" or not text
                check_value = check_item

            # stringify check value and omit long text
            omitted_check_value = omit_long_data(str(check_value))

            # comparator
            assert_method = validator.method

            # functions found in package httprunner.builtin will be added to functions mapping too
            assert_func = get_mapping_function(assert_method, functions_mapping)

            # expect item
            expect_item = validator.expect
            # parse expected value with config/teststep/extracted variables
            expect_value = parse_data(expect_item, variables_mapping, functions_mapping)
            # omit expect value
            omitted_expect_value = omit_long_data(str(expect_value))

            # message
            message = validator.message
            # parse message with config/teststep/extracted variables
            message = parse_data(message, variables_mapping, functions_mapping)

            validate_msg = f"assert {check_item} {assert_method} {omitted_expect_value}({type(expect_value).__name__})"

            validator_dict = {
                validation_settings.content.keys.result: None,
                validation_settings.content.keys.assert_: {
                    validation_settings.content.keys.actual_value: check_value,
                    validation_settings.content.keys.comparator: assert_method,
                    validation_settings.content.keys.expect_value: expect_value,
                },
                validation_settings.content.keys.message: message,
                validation_settings.content.keys.jmespath_: check_item,
                validation_settings.content.keys.raw_expect_value: expect_item,
            }

            try:
                assert_func(check_value, expect_value, message, **validator.config)
                validate_msg += "\t==> pass"
                logger.info(validate_msg)
                validator_dict["Result"] = emojis.success
            except AssertionError as ex:
                validate_pass = False
                validator_dict["Result"] = emojis.failure
                validate_msg += "\t==> fail"
                allure_failure_message = f"""\
* JMESPath 及断言方法
{check_item} -> {assert_method}

* 预期值 ({type(expect_value).__name__})
{omitted_expect_value}

* 实际值 ({type(check_value).__name__})
{omitted_check_value}

* 错误信息
{str(ex) if str(ex) else "NA"}
                """
                validate_msg += f"\n{allure_failure_message}"

                logger.error(validate_msg)
                failures.append(allure_failure_message)

            self.validation_results["validate_extractor"].append(validator_dict)

        if not validate_pass:
            # add headers for each element if more than 1 exist
            if len(failures) > 1:
                indexed_failures = []
                for i, validator in enumerate(failures, start=1):
                    validator = f"第 {i} 个失败的断言\n---------------\n" + validator
                    indexed_failures.append(validator)
            else:
                indexed_failures = failures

            # add new lines after header 'httprunner.exceptions.ValidationFailure'
            indexed_failures[0] = "\n\n" + indexed_failures[0]

            # separate each failure with three new lines
            failures_string = "\n\n\n".join([failure for failure in indexed_failures])

            raise ValidationFailure(failures_string)
