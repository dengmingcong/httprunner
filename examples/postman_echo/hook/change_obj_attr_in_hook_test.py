from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase

from ...debugtalk import CustomClass


class BaseCase(HttpRunner):

    config = Config("base case").base_url("https://postman-echo.com").verify(False)

    teststeps = [
        Step(
            RunRequest("change obj attr in hook")
            .post("/post")
            .with_json({})
            .teardown_hook("${modify_obj_attr($obj)}")
            .validate()
            .assert_equal("status_code", 200)
        ),
    ]


class TestChangeObjAttrInHook(HttpRunner):

    config = (
        Config("test change obj attr in hook")
        .variables(**{"obj": CustomClass("foo")})
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(RunTestCase("base case").call(BaseCase)),
        Step(
            RunRequest("request with changed obj attr")
            .post("/post")
            .with_json(
                {
                    "id": "${obj.id}",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.id", 100)
        ),
    ]
