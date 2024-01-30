import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import OverrideReservedVariableError
from httprunner.testcase import HttpRunnerRequest, RequestConfig


class PostmanEchoPost(HttpRunnerRequest):
    config = (
        RequestConfig("${api['name']}")
        .with_resource(
            "api",
            "${mimic_api()}",
            "extract_variables_from_api",
        )
        .variables(
            **{
                "foo": "foo_new",
            }
        )
    )
    request = RunRequest("").post("/post").with_json("${eval_var($__preset_json)}")


class TestWithResource(HttpRunner):
    config = (
        Config("test with_resource()")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            PostmanEchoPost()
            .update_json_object({"BAZ": "$baz"})
            .validate()
            .assert_equal("body.json.FOO", "foo_new")
            .assert_equal("body.json.BAR", "bar")
            .assert_equal("body.json.BAZ", "baz")
            .assert_equal("body.json.method", "POST")
        ),
    ]


@pytest.mark.xfail(raises=OverrideReservedVariableError)
class TestResourceNameWasOverriden(HttpRunner):
    config = (
        Config("test resource_name was overriden")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            PostmanEchoPost()
            .with_variables(**{"api": "any"})
            .update_json_object({"BAZ": "$baz"})
            .validate()
            .assert_equal("body.json.FOO", "foo_new")
            .assert_equal("body.json.BAR", "bar")
            .assert_equal("body.json.BAZ", "baz")
            .assert_equal("body.json.method", "POST")
        ),
    ]
