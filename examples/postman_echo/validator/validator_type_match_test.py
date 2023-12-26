from httprunner import HttpRunner, Config, Step, RunRequest


class TestValidatorTypeMatch(HttpRunner):

    config = (
        Config("test validator assert_type_match")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("expected value is a type")
            .post("/post")
            .with_headers(
                **{
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            )
            .with_data("foo=bar")
            .validate()
            .assert_equal("status_code", 200)
            .assert_type_match("body.form.foo", str)
        ),
    ]
