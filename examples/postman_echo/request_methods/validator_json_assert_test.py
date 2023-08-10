import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


class TestValidatorJsonAssert(HttpRunner):

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
            .assert_json_contains(
                "body.json",
                (
                    {"foo": "foo", "bar": [4, 3, 2, 1], "baz": 1.0},
                    {"ignore_numeric_type_changes": True},
                ),
            )
            .assert_json_equal(
                "body.json",
                (
                    {
                        "foo": "foo",
                        "bar": [1, 2, 3, 4],
                        "baz": 1.0,
                    },
                    {"ignore_numeric_type_changes": True},
                ),
            )
        ),
    ]


@pytest.mark.xfail(raises=ValidationFailure)
class TestValidatorIsCloseFail(HttpRunner):

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
            .assert_json_contains("body.json", {"bar": [4, 4, 2, 1], "baz": 1.0})
        ),
    ]
