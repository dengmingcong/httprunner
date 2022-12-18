from httprunner import __version__


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


def get_raw_data_name(raw_data: dict) -> str:
    """
    Test extracted value containing dollar as function argument.
    """
    return raw_data["name"]


def get_json(foo, bar):
    return {
        "foo": foo,
        "bar": bar
    }
