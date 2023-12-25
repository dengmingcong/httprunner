import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import MultiStepsFailedError


@pytest.mark.xfail(raises=MultiStepsFailedError)
class TestCaseUpdateUrlOrigin(HttpRunner):

    config = (
        Config("test update url origin")
        .variables(**{"foo": 1, "bar": 2, "baz": 3})
        .base_url("http://bad-netloc.com")
        .verify(False)
        .continue_on_failure()
    )

    teststeps = [
        Step(
            RunRequest("update origin")
            .post("/post")
            .with_origin("https://postman-echo.com")
            .with_json({"foo": "$foo", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "bad")
        ),
        Step(
            RunRequest("don't update origin")
            .post("https://postman-echo.com/post")
            .with_json({"foo": "$foo", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "bad")
        ),
    ]


if __name__ == "__main__":
    TestCaseUpdateUrlOrigin().test_start()
