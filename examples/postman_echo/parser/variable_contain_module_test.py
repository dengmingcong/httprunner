import json

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.testcase import HttpRunnerRequest, RequestConfig


class TestConfigVariableContainModule(HttpRunner):

    config = (
        Config("test config variable contain module")
        .variables(**{"foo": {1: 1}, "json": json})
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("config variable contain module")
            .post("/post")
            .with_json({"data": "${pyexp(json.dumps(foo))}"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.data", '{"1": 1}')
        ),
    ]


class BaseRequest(HttpRunnerRequest):
    config = RequestConfig("base request").variables(**{"foo": {1: 1}, "json": json})
    request = (
        RunRequest("").post("/post").with_json({"data": "${pyexp(json.dumps(foo))}"})
    )


class TestHttpRunnerRequestConfigContainModule(HttpRunner):
    config = (
        Config("test HttpRunnerRequest config contain module")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(BaseRequest()),
    ]
