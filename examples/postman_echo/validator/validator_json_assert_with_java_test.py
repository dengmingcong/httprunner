import pytest

from httprunner import Config, HttpRunner, RunRequest, Step
from httprunner.exceptions import ValidationFailure


class TestValidatorJsonAssertWithJava(HttpRunner):
    config = (
        Config("validate with json assert with java")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with json assert")
            .post("/post")
            .with_json({"foo": "foo", "bar": [1, 2, 3, 4], "baz": 1})
            .validate()
            .assert_equal("status_code", 200)
            .assert_json_contains_with_java(
                "body.json",
                {"foo": "foo", "bar": [4, 3, 2, 1], "baz": 1.0},
            )
            .assert_json_equal_with_java(
                "body.json",
                {
                    "foo": "foo",
                    "bar": [1, 2, 3, 4],
                    "baz": 1.0,
                },
            )
        ),
    ]


@pytest.mark.xfail(raises=ValidationFailure)
class TestValidateFailed(HttpRunner):
    config = (
        Config("validate with json assert")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with json assert")
            .post("/post")
            .with_json({"foo": "foo", "bar": [1, 2, 3, 4], "baz": 1})
            .validate()
            .assert_equal("status_code", 200)
            .assert_json_contains_with_java(
                "body.json", {"bar": [4, 4, 2, 1], "baz": 1.0}
            )
        ),
    ]
