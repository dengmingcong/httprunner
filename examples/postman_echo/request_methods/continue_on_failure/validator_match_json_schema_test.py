import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import MultiStepsFailedError


@pytest.mark.xfail(raises=MultiStepsFailedError)
class TestValidatorMatchSchema(HttpRunner):
    config = (
        Config("test validator match schema")
        .base_url("https://postman-echo.com")
        .verify(False)
        .continue_on_failure()
    )

    teststeps = [
        Step(
            RunRequest("instance does not match schema")
            .post("/post")
            .with_json({"name": "Eggs", "price": "Invalid"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_match_json_schema(
                "body.json",
                {
                    "type": "object",
                    "properties": {
                        "price": {"type": "number"},
                        "name": {"type": "string"},
                    },
                },
            )
        ),
        Step(
            RunRequest("schema itself is invalid")
            .post("/post")
            .with_json({"name": "Eggs", "price": "Invalid"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_match_json_schema(
                "body.json",
                {
                    "type": "objects",
                    "properties": {
                        "price": {"type": "number"},
                        "name": {"type": "string"},
                    },
                },
            )
        ),
    ]
