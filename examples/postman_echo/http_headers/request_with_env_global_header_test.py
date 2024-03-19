import os
from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.configs.http import GlobalHttpSettings, global_http_settings


os.environ["GLOBAL_HTTP_HEADERS"] = '{"x-foo": "FOO", "x-bar": "BAR"}'
settings = GlobalHttpSettings()
global_http_settings.headers = settings.headers


class TestCaseRequestWithEnvGlobalHeader(HttpRunner):
    """Test request with env global headers.

    Note:
        Before running this testcase, make sure env variable `global_http_headers` was set,
        and its value is json string `'{"x-foo": "FOO"}'`.
        For example, in terminal, run: export GLOBAL_HEADERS='{"hello": "world"}'.
    """

    config = (
        Config("request methods testcase with env global header")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("request with global header")
            .get("/get")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('body.headers."x-foo"', "FOO")
            .assert_equal('body.headers."x-bar"', "BAR")
        ),
    ]
