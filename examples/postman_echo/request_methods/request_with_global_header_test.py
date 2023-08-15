from httprunner import HttpRunner, Config, Step, RunRequest


class TestCaseRequestWithGlobalHeader(HttpRunner):

    config = (
        Config("request methods testcase with global header")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("request with global header")
            .get("/get")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('body.headers."x-global-header"', "FOO")
        ),
    ]
