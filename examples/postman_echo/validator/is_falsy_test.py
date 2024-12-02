from httprunner import Config, HttpRunner, RunRequest, Step


class TestValidatorIsFalsy(HttpRunner):
    config = (
        Config("test validate with is_falsy")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("validate with is_falsy")
            .post("/post")
            .with_json({"foo": [], "bar": False, "baz": 0})
            .validate()
            .assert_equal("status_code", 200)
            .assert_is_falsy("body.json.foo")
            .assert_is_falsy("body.json.bar")
            .assert_is_falsy("body.json.baz")
        ),
    ]
