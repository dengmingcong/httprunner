import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


class TestValidatorNoKeysDuplicate(HttpRunner):

    config = (
        Config("validate with no_keys_duplicate")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with is_close")
            .post("/post")
            .with_json({"foo": [1, 2, 3]})
            .validate()
            .assert_equal("status_code", 200)
            .assert_no_keys_duplicate("body.json.foo")
        ),
    ]


@pytest.mark.xfail(raises=ValidationFailure)
class TestValidatorNoKeysDuplicateFail(HttpRunner):

    config = (
        Config("validate with no_keys_duplicate")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with is_close")
            .post("/post")
            .with_json({"foo": [1, 2, 4, 2, 4, 5]})
            .validate()
            .assert_equal("status_code", 200)
            .assert_no_keys_duplicate("body.json.foo")
        ),
    ]
