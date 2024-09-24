import pytest

from httprunner import Config, HttpRunner, RunRequest, Step
from httprunner.pyproject import load_pyproject_toml


@pytest.fixture(autouse=True)
def set_http_headers():
    load_pyproject_toml()["tool"]["httprunner"] = {
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
