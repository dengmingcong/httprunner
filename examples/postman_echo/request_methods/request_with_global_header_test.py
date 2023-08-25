import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.pyproject import pyproject_toml_data


@pytest.fixture(autouse=True)
def set_http_headers():
    pyproject_toml_data["tool"]["httprunner"] = {
        "http-headers": {"X-Global-Header": "FOO"}
    }
    yield


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
