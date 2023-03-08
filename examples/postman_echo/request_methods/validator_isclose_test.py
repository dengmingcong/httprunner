import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


class TestValidatorIsClose(HttpRunner):

    config = (
        Config("validate with is_close")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with is_close")
            .post("/post")
            .with_json({
                "foo": 20
            })
            .validate()
            .assert_equal("status_code", 200)
            .assert_is_close("body.json.foo", (10, 10))
        ),
    ]


@pytest.mark.xfail(raises=ValidationFailure)
class TestValidatorIsCloseFail(HttpRunner):

    config = (
        Config("validate with is_close")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with is_close")
            .post("/post")
            .with_json({
                "foo": 20
            })
            .validate()
            .assert_equal("status_code", 200)
            .assert_is_close("body.json.foo", (10, 9.9))
        ),
    ]
