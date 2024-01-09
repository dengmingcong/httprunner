from httprunner import HttpRunner, Config, Step, RunRequest


class TestParametrizeVarsWillNotOverwriteContextVars(HttpRunner):
    config = (
        Config("test parametrizing vars will not overwrite context vars")
        .base_url("https://www.postman-echo.com")
        .variables(**{"foo": 0})
    )
    teststeps = [
        Step(
            RunRequest("parametrize foo")
            .parametrize("foo", [1, 2])
            .post("/post")
            .with_json({"foo": "$foo"})
            .validate()
            .assert_equal("body.json.foo", "$foo")
        ),
        Step(
            RunRequest("still use config vars `foo`")
            .post("/post")
            .with_json({"foo": "$foo"})
            .validate()
            .assert_equal("body.json.foo", 0)
        ),
    ]
