# NOTE: Generated By HttpRunner v3.1.4
# FROM: request_methods/request_with_testcase_reference.yml


import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase

from request_methods.request_with_functions_test import (
    TestCaseRequestWithFunctions as RequestWithFunctions,
)


class TestCaseRequestWithTestcaseReference(HttpRunner):

    config = (
        Config("request methods testcase: reference testcase")
        .variables(
            **{
                "foo1": "testsuite_config_bar1",
                "expect_foo1": "testsuite_config_bar1",
                "expect_foo2": "config_bar2",
            }
        )
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("request with functions")
            .with_variables(
                **{"foo1": "testcase_ref_bar1", "expect_foo1": "testcase_ref_bar1"}
            )
            .setup_hook("${sleep(0.1)}")
            .call(RequestWithFunctions)
            .export("foo3")
            .teardown_hook("${sleep(0.2)}")
            .export(*["app_version_1", "app_version_3"])
        ),
        Step(
            RunRequest("post form data")
            .with_variables(**{"foo1": "bar1"})
            .post("/post")
            .with_headers(
                **{
                    "User-Agent": "HttpRunner/${get_httprunner_version()}",
                }
            )
            .with_json(
                {
                    "app_version_1": "$app_version_1",
                    "app_version_3": "$app_version_3",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
    ]


if __name__ == "__main__":
    TestCaseRequestWithTestcaseReference().test_start()
