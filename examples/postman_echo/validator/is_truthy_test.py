from httprunner import HttpRunner, Config, Step, RunRequest


class TestValidatorIsTruthy(HttpRunner):

    config = (
        Config("test validate with is_truthy")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with is_truthy")
            .post("/post")
            .with_json({"foo": [1, 2, 3], "bar": True, "baz": 1})
            .validate()
            .assert_equal("status_code", 200)
            .assert_is_truthy("body.json.foo")
            .assert_is_truthy("body.json.bar")
            .assert_is_truthy("body.json.baz")
        ),
    ]
