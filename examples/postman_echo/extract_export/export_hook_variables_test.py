from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


from ..request_methods.base_request import (
    TestCaseRequestAndExport as RequestAndExport,
)


class TestExportHookVariables(HttpRunner):

    config = (
        Config("test export hook variables")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("export testcase hook variables")
            .setup_hook("${gen_hook_variable(case_setup_hook)}", "case_setup_hook")
            .call(RequestAndExport)
            .teardown_hook(
                "${gen_hook_variable(case_teardown_hook)}", "case_teardown_hook"
            )
            .export("case_setup_hook", "case_teardown_hook")
        ),
        Step(
            RunRequest("export request hook variables - export")
            .setup_hook(
                "${gen_hook_variable(request_setup_hook)}", "request_setup_hook"
            )
            .post("/post")
            .with_json(
                {
                    "setup": "$case_setup_hook",
                    "teardown": "$case_teardown_hook",
                }
            )
            .teardown_hook(
                "${gen_hook_variable(request_teardown_hook)}", "request_teardown_hook"
            )
            .export()
            .variable("request_setup_hook")
            .variable("request_teardown_hook")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.setup", "case_setup_hook")
            .assert_equal("body.json.teardown", "case_teardown_hook")
        ),
        Step(
            RunRequest("export request hook variables - use")
            .post("/post")
            .with_json(
                {
                    "setup": "$request_setup_hook",
                    "teardown": "$request_teardown_hook",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.setup", "request_setup_hook")
            .assert_equal("body.json.teardown", "request_teardown_hook")
        ),
    ]
