import os
import random
import string
import time
import uuid
from typing import Union

from dotwiz import DotWiz
from loguru import logger

from httprunner import __version__
from httprunner.parser import ParseMe


def get_httprunner_version():
    return __version__


def sum_two(m, n):
    return int(m) + int(n)


def get_testcase_config_variables():
    return {"foo1": "testcase_config_bar1", "foo2": "testcase_config_bar2"}


def get_testsuite_config_variables():
    return {"foo1": "testsuite_config_bar1", "foo2": "testsuite_config_bar2"}


def get_app_version():
    return [3.1, 3.0]


def calculate_two_nums(a, b=1):
    return [a + b, b - a]


def get_raw_func():
    return "${calculate_two_nums(1, 1)}"


def get_raw_dict():
    return {"foo": "$bar"}


def get_raw_data_name(raw_data: dict) -> str:
    """
    Test extracted value containing dollar as function argument.
    """
    return raw_data["name"]


def get_json(foo, bar):
    return {"foo": foo, "bar": bar}


def get_variables_from_string():
    return {"foo": "foo", "config_model": "${sku.config_model}"}


def get_variables_from_str():
    return {"config_model": "${sku.config_model}"}


def get_httpbin_server():
    return "https://httpbin.org"


def setup_testcase(variables):
    logger.info(f"setup_testcase, variables: {variables}")
    variables["request_id_prefix"] = str(int(time.time()))


def teardown_testcase():
    logger.info("teardown_testcase.")


def setup_teststep(request, variables):
    logger.info(f"setup_teststep, request: {request}, variables: {variables}")
    request.setdefault("headers", {})
    request_id_prefix = variables["request_id_prefix"]
    request["headers"]["HRUN-Request-ID"] = request_id_prefix + "-" + str(uuid.uuid4())


def teardown_teststep(response):
    logger.info(f"teardown_teststep, response status code: {response.status_code}")


def sum_status_code(status_code, expect_sum):
    """sum status code digits
    e.g. 400 => 4, 201 => 3
    """
    sum_value = 0
    for digit in str(status_code):
        sum_value += int(digit)

    assert sum_value == expect_sum


def is_status_code_200(status_code):
    return status_code == 200


os.environ["TEST_ENV"] = "PRODUCTION"


def skip_test_in_production_env():
    """skip this test in production environment"""
    return os.environ["TEST_ENV"] == "PRODUCTION"


def get_user_agent():
    return ["iOS/10.1", "iOS/10.2"]


def gen_app_version():
    return [{"app_version": "2.8.5"}, {"app_version": "2.8.6"}]


def get_account():
    return [
        {"username": "user1", "password": "111111"},
        {"username": "user2", "password": "222222"},
    ]


def get_account_in_tuple():
    return [("user1", "111111"), ("user2", "222222")]


def gen_random_string(str_len):
    random_char_list = []
    for _ in range(str_len):
        random_char = random.choice(string.ascii_letters + string.digits)
        random_char_list.append(random_char)

    random_string = "".join(random_char_list)
    return random_string


def setup_hook_add_kwargs(request):
    request["key"] = "value"


def setup_hook_remove_kwargs(request):
    request.pop("key")


def teardown_hook_sleep_N_secs(response, n_secs):
    """sleep n seconds after request"""
    if response.status_code == 200:
        time.sleep(0.1)
    else:
        time.sleep(n_secs)


def hook_print(msg):
    print(msg)


def modify_request_json(request, os_platform):
    request["json"]["os_platform"] = os_platform


def setup_hook_httpntlmauth(request):
    if "httpntlmauth" in request:
        from requests_ntlm import HttpNtlmAuth

        auth_account = request.pop("httpntlmauth")
        request["auth"] = HttpNtlmAuth(
            auth_account["username"], auth_account["password"]
        )


def alter_response(response):
    response.status_code = 500
    response.headers["Content-Type"] = "html/text"
    response.body["headers"]["Host"] = "127.0.0.1:8888"
    response.new_attribute = "new_attribute_value"
    response.new_attribute_dict = {"key": 123}


def alter_response_302(response):
    response.status_code = 500
    response.headers["Content-Type"] = "html/text"
    response.text = "abcdef"
    response.new_attribute = "new_attribute_value"
    response.new_attribute_dict = {"key": 123}


def alter_response_error(response):
    # NameError
    pass


def gen_variables():
    return {"var_a": 1, "var_b": 2}


def gen_trace_id(
    format_: str = "TIMESTAMP_IN_MILLISECOND",
) -> Union[str, int]:
    """Returns trace id based on id type."""
    if format_ == "TIMESTAMP_IN_SECOND":
        return int(time.time())
    elif format_ == "TIMESTAMP_IN_MILLISECOND":
        return str(int(time.time() * 1000))
    elif format_ == "UUID4":
        return uuid.uuid4().hex
    elif format_ == "UUID4_URN":
        return uuid.uuid4().urn


def gen_hook_variable(hook: str):
    return hook


class CustomClass(ParseMe):
    def __init__(self, foo):
        self.id = None
        self.foo = foo


def modify_obj_attr(obj: CustomClass):
    obj.id = 100


def mimic_api():
    """Mimic api docs object."""
    return DotWiz(
        {
            "name": "apiName",
            "method": "POST",
            "variables": [
                {"identifier": "foo", "value": "foo"},
                {"identifier": "bar", "value": "bar"},
                {"identifier": "baz", "value": "baz"},
            ],
            "preset_json": {"FOO": "$foo", "BAR": "$bar", "method": "${api['method']}"},
        }
    )


def mimic_another_api():
    """Mimic api docs object."""
    return DotWiz(
        {
            "name": "anotherApiName",
            "method": "GET",
            "variables": [
                {"identifier": "foo", "value": "foo"},
                {"identifier": "bar", "value": "bar-another"},
                {"identifier": "quu", "value": "quu"},
            ],
            "preset_json": {
                "FOO": "$foo",
                "BAR": "$bar",
                "method": "${api['method']}",
                "QUU": "$quu",
            },
        }
    )


def extract_variables_from_api(api: DotWiz) -> dict:
    """Extract variables from api."""
    variables = {
        variable["identifier"]: variable["value"] for variable in api["variables"]
    }
    variables["__preset_json"] = api["preset_json"].to_dict()
    return variables
