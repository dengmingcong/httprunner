import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


@pytest.mark.xfail(raises=ValidationFailure)
class TestCasePopJsonObjectKeys(HttpRunner):

    config = (
        Config("test pop json object keys")
        .variables(**{"foo": 1, "bar": 2, "baz": 3})
        .base_url("https://postman-echo.com")
        .verify(False)
        .continue_on_failure()
    )

    teststeps = [
        Step(
            RunRequest("with_json has not been called")
            .post("/post")
            .with_json({"foo": "$foo", "bar": "$bar"})
            .pop_json_object_keys("foo")
            .validate()
            .assert_equal("body.json.bar", "bad")
        ),
    ]


if __name__ == "__main__":
    TestCasePopJsonObjectKeys().test_start()
