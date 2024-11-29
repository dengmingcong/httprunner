import pytest

from httprunner import Config, HttpRunner, RunRequest, Step
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
            .assert_json_contains(
                "body.json",
                {"foo": "foo", "bar": [4, 3, 2, 1], "baz": 1.0},
                ignore_numeric_type_changes=True,
            )
            .assert_json_equal(
                "body.json",
                {
                    "foo": "foo",
                    "bar": [1, 2, 3, 4],
                    "baz": 1.0,
                },
                ignore_numeric_type_changes=True,
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
            .assert_json_contains("body.json", {"bar": [4, 4, 2, 1], "baz": 1.0})
        ),
    ]


@pytest.mark.xfail(raises=ValidationFailure)
class TestFailMessage(HttpRunner):
    config = (
        Config("test error message format")
        .base_url("https://postman-echo.com")
        .verify(False)
        .continue_on_failure()
    )

    teststeps = [
        Step(
            RunRequest("test error message format")
            .post("/post")
            .with_json(
                {
                    "type_changes01": 1.1,
                    "type_changes02": 1.1,
                    "values_changed01": "new",
                    "values_changed02": "new",
                    "item_added01": "this item is unexpected",
                    "item_added02": "this item is unexpected",
                    "list_not_expected": [1, 2, 3, 3],
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_json_equal(
                "body.json",
                {
                    "type_changes01": 1,
                    "type_changes02": 1,
                    "values_changed01": "old",
                    "values_changed02": "old",
                    "item_removed01": "this item is missing",
                    "item_removed02": "this item is missing",
                    "list_not_expected": [1, 2, 3, 4],
                },
                ignore_string_type_changes=True,
            )
        ),
        Step(
            RunRequest("list not expected")
            .post("/post")
            .with_json(
                {
                    "list_not_expected": [1, 2, 3, 3],
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_json_contains(
                "body.json",
                {
                    "list_not_expected": [1, 2, 3, 4],
                },
                ignore_string_type_changes=True,
            )
        ),
    ]
