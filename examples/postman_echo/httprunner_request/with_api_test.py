from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.testcase import HttpRunnerRequest, RequestConfig


class PostmanEchoPost(HttpRunnerRequest):
    config = (
        RequestConfig("${api['name']}")
        .with_api(
            "${mimic_api()}",
            "extract_variables_from_api",
            "extract_preset_json_from_api",
        )
        .variables(
            **{
                "foo": "foo_new",
            }
        )
    )
    request = RunRequest("").post("/post").with_json("${eval_var($preset_json)}")


class TestWithApi(HttpRunner):
    config = (
        Config("test with_api()").base_url("https://postman-echo.com").verify(False)
    )

    teststeps = [
        Step(
            PostmanEchoPost()
            .update_json_object({"BAZ": "$baz"})
            .validate()
            .assert_equal("body.json.FOO", "foo_new")
            .assert_equal("body.json.BAR", "bar")
            .assert_equal("body.json.BAZ", "baz")
        ),
    ]
