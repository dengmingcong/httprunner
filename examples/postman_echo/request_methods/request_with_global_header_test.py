import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.builtin.dictionary import is_keys_exist
from httprunner.pyproject import pyproject_toml


@pytest.fixture(autouse=True)
def set_http_headers():
    if is_keys_exist(pyproject_toml, "tool", "httprunner", "http-headers"):
        yield
    else:
        pyproject_toml["tool"]["httprunner"] = {
            "http-headers": {"X-Global-Header": "FOO"}
        }
        yield
        pyproject_toml["tool"]["httprunner"].pop("http-headers")


class TestCaseRequestWithGlobalHeader(HttpRunner):

    config = (
        Config("request methods testcase with global header")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("request with global header")
            .get("/get")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('body.headers."x-global-header"', "FOO")
        ),
    ]
