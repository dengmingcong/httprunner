from dotwiz import DotWiz

from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class SubTestCase(HttpRunner):
    config = Config("base case").base_url("https://www.postman-echo.com")
    teststeps = [
        Step(
            RunRequest("sub test case")
            .post("/post")
            .with_json({"foo": "$foo", "config_model": "$config_model"})
            .validate()
            .assert_equal("body.json.foo", "foo")
            .assert_equal("body.json.config_model", "core400")
        ),
    ]


class TestWithRawVariables(HttpRunner):
    config = (
        Config("test request with raw variables")
        .base_url("https://www.postman-echo.com")
        .variables(**{"sku": DotWiz({"config_model": "core400"})})
    )
    teststeps = [
        Step(
            RunRequest("with_raw_variables in RunRequest")
            .with_variables_raw("${get_variables_from_string()}")
            .post("/post")
            .with_json({"foo": "$foo", "config_model": "$config_model"})
            .validate()
            .assert_equal("body.json.foo", "foo")
            .assert_equal("body.json.config_model", "core400")
        ),
        Step(
            RunTestCase("with_raw_variables in RunTestCase")
            .with_variables(**{"foo": "foo"})
            .with_variables_raw("${get_variables_from_str()}")
            .call(SubTestCase)
        ),
    ]
