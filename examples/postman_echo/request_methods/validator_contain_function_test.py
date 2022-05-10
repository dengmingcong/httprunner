from httprunner import HttpRunner, Config, Step, RunRequest


class TestValidatorContainFunction(HttpRunner):

    config = (
        Config("test validator contains function")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("expected value is a function")
            .post("/post")
            .with_data("foo=bar")
            .validate()
            .assert_equal("status_code", 200)
            .assert_not_equal("body.form.foo", getattr)
        ),
    ]


if __name__ == "__main__":
    TestValidatorContainFunction().test_start()
