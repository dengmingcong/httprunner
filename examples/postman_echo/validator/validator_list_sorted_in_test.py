import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


class TestValidatorListSortedIn(HttpRunner):

    config = (
        Config("validate with list_sorted_in")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with list_sorted_in")
            .post("/post")
            .with_json({"foo": [1, 2, 3]})
            .validate()
            .assert_equal("status_code", 200)
            .assert_list_sorted_in("body.json.foo", "ASC")
        ),
    ]


@pytest.mark.xfail(raises=ValidationFailure)
class TestValidatorListSortedInFail(HttpRunner):

    config = (
        Config("validate with list_sorted_in")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with list_sorted_in")
            .post("/post")
            .with_json({"foo": [1, 2, 3]})
            .validate()
            .assert_equal("status_code", 200)
            .assert_list_sorted_in("body.json.foo", "DSC")
        ),
    ]
