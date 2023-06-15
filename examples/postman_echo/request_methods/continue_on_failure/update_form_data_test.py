import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


@pytest.mark.xfail(raises=ValidationFailure)
class TestCaseUpdateFormData(HttpRunner):

    config = (
        Config("test update json")
        .variables(**{"foo": "1", "bar": "2", "baz": "3"})
        .base_url("https://postman-echo.com")
        .verify(False)
        .continue_on_failure()
    )

    teststeps = [
        Step(
            RunRequest("with_data has been called")
            .post("/post")
            .with_data({"foo": "3", "baz": "$baz"})
            .update_form_data({"foo": "$foo", "bar": "$bar"})
            .validate()
            .assert_equal("body.form.foo", "$foo")
            .assert_equal("body.form.bar", "$bar")
            .assert_equal("body.form.baz", "bad")
        ),
    ]


if __name__ == "__main__":
    TestCaseUpdateFormData().test_start()
