from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.testcase import HttpRunnerRequest, RequestConfig


class PostmanEchoPost(HttpRunnerRequest):
    config = (
        RequestConfig("${api['name']}")
        .with_resource(
            "api",
            "${mimic_api()}",
            "extract_variables_from_api",
        )
        .with_resource(
            "another_api",
            "${mimic_another_api()}",
            "extract_variables_from_api",
        )
        .variables(
            **{
                "foo": "foo_new",
            }
        )
    )
    request = RunRequest("").post("/post").with_json("$__preset_json")


class TestWithResource(HttpRunner):
    config = (
        Config("test calling with_resource() multiple times")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            PostmanEchoPost("latter resource overrides previous one")
            .update_json_object({"BAZ": "$baz"})
            .validate()
            .assert_equal(
                "body.json.FOO", "foo_new", "RunRequest.variables > resource variables"
            )
            .assert_equal(
                "body.json.BAR", "bar-another", "latter resource overrides previous one"
            )
            .assert_equal("body.json.BAZ", "baz", "update_json_object() take effect")
            .assert_equal("body.json.method", "POST", "parse preset_json correctly")
        ),
    ]
