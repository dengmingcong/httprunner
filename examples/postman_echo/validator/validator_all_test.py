import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


class TestValidatorAll(HttpRunner):

    config = (
        Config("validate with all").base_url("https://postman-echo.com").verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with all")
            .post("/post")
            .with_json({"foo": [1, 2, 3]})
            .validate()
            .assert_equal("status_code", 200)
            .assert_all("body.json.foo")
        ),
        Step(
            RunRequest("validate with all and processor")
            .post("/post")
            .with_json({"foo": 1, "bar": 2})
            .validate()
            .assert_equal("status_code", 200)
            .assert_all("body.json", lambda x: [v is not None for k, v in x.items()])
        ),
        Step(
            RunRequest("validate with all and processor and kwargs")
            .post("/post")
            .with_json({"foo": 1, "bar": 2, "baz": None})
            .validate()
            .assert_equal("status_code", 200)
            .assert_all(
                "body.json",
                (
                    lambda x, keys: [v is not None for k, v in x.items() if v in keys],
                    {"keys": ["foo", "bar"]},
                ),
            )
        ),
    ]


@pytest.mark.xfail(raises=ValidationFailure)
class TestValidatorAllFail(HttpRunner):

    config = (
        Config("validate with all").base_url("https://postman-echo.com").verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with all")
            .post("/post")
            .with_json({"foo": [0, 1, 2]})
            .validate()
            .assert_equal("status_code", 200)
            .assert_all("body.json.foo")
        ),
    ]


@pytest.mark.xfail(raises=ValidationFailure)
class TestValidatorAllAndProcessorFail(HttpRunner):

    config = (
        Config("validate with all").base_url("https://postman-echo.com").verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with all")
            .post("/post")
            .with_json({"foo": 1, "bar": None})
            .validate()
            .assert_equal("status_code", 200)
            .assert_all(
                "body.json",
                lambda x: [v is not None for k, v in x.items()],
                "每一个键的值都应该不为 None",
            )
        ),
    ]
