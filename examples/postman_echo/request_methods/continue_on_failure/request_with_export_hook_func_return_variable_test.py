# NOTE: Generated By HttpRunner v3.1.4
# FROM: request_methods/request_with_functions.yml


import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import MultiStepsFailedError


@pytest.mark.xfail(raises=MultiStepsFailedError)
class TestCaseRequestWithFunctions(HttpRunner):

    config = (
        Config("request methods testcase with functions")
        .variables(
            **{
                "foo1": "config_bar1",
                "foo2": "config_bar2",
                "expect_foo1": "config_bar1",
                "expect_foo2": "config_bar2",
            }
        )
        .base_url("https://postman-echo.com")
        .verify(False)
        .export(*["foo3"])
        .locust_weight(2)
        .continue_on_failure()
    )

    teststeps = [
        Step(
            RunRequest("get with params")
            .with_variables(
                **{"foo1": "bar11", "foo2": "bar21", "sum_v": "${sum_two(1, 2)}"}
            )
            .get("/get")
            .with_params(**{"foo1": "$foo1", "foo2": "$foo2", "sum_v": "$sum_v"})
            .with_headers(**{"User-Agent": "HttpRunner/${get_httprunner_version()}"})
            .teardown_hook("${get_app_version()}", "app_version")
            .extract()
            .with_jmespath("body.args.foo2", "foo3")
            .export()
            .variable("app_version")
            .variable("app_version", "app_version_rename")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.args.foo1", "bar11")
            .assert_equal("body.args.sum_v", "4")
            .assert_equal("body.args.foo2", "bar21")
        ),
        Step(
            RunRequest("reference vars exported from previous step")
            .with_variables(**{"foo1": "bar12", "foo3": "bar32"})
            .post("/post")
            .with_headers(
                **{
                    "User-Agent": "HttpRunner/${get_httprunner_version()}",
                }
            )
            .with_json(
                {
                    "app_version": "$app_version",
                    "app_version_rename": "$app_version_rename",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.app_version", [3.1, 3.2])
        ),
        Step(
            RunRequest("post form data")
            .with_variables(**{"foo2": "bar23"})
            .post("/post")
            .with_headers(
                **{
                    "User-Agent": "HttpRunner/${get_httprunner_version()}",
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            )
            .with_data("foo1=$foo1&foo2=$foo2&foo3=$foo3")
            .validate()
            .assert_equal("status_code", 200, "response status code should be 200")
            .assert_equal("body.form.foo1", "$expect_foo1")
            .assert_equal("body.form.foo2", "bar23")
            .assert_equal("body.form.foo3", "bar22")
        ),
    ]


if __name__ == "__main__":
    TestCaseRequestWithFunctions().test_start()
