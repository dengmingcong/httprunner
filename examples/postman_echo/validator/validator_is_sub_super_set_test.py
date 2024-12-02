import pytest

from httprunner import Config, HttpRunner, RunRequest, Step
from httprunner.exceptions import ValidationFailure


class TestValidatorIsSubSuperSet(HttpRunner):
    config = (
        Config("validate with is_subset and is_superset")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate is_subset")
            .with_variables(expected=[1, 2, 3, 4])
            .post("/post")
            .with_json({"foo01": [1, 2, 2], "foo02": [1, 2, 3]})
            .validate()
            .assert_equal("status_code", 200)
            .assert_is_truthy_and_subset("body.json.foo01", "$expected")
            .assert_is_truthy_and_subset("body.json.foo02", "$expected")
        ),
        Step(
            RunRequest("validate is_superset")
            .with_variables(expected=[1, 2, 3])
            .post("/post")
            .with_json({"foo01": [1, 2, 3, 3, 4], "foo02": [1, 2, 3]})
            .validate()
            .assert_equal("status_code", 200)
            .assert_is_truthy_and_superset("body.json.foo01", "$expected")
            .assert_is_truthy_and_superset("body.json.foo02", "$expected")
        ),
    ]


@pytest.mark.xfail(raises=ValidationFailure)
class TestValidatorIsSubSuperSetFail(HttpRunner):
    config = (
        Config("validate with is_subset and is_superset")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with is_subset")
            .post("/post")
            .with_json({"foo01": [1, 2, 3], "foo02": None, "foo03": []})
            .validate()
            .assert_equal("status_code", 200)
            .assert_is_truthy_and_subset("body.json.foo01", [1, 2, 4])
            .assert_is_truthy_and_superset("body.json.foo01", [1, 2, 4])
            .assert_is_truthy_and_subset("body.json.foo02", [1, 2, 3])
            .assert_is_truthy_and_superset("body.json.foo02", [1, 2, 3])
            .assert_is_truthy_and_subset("body.json.foo03", [1, 2, 3])
            .assert_is_truthy_and_superset("body.json.foo03", [1, 2, 3])
        ),
    ]
