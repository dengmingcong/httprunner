# NOTE: Generated By HttpRunner v3.1.4
# FROM: request_methods/request_with_functions.yml


from httprunner import HttpRunner, Config, Step, RunRequest


class TestCaseRequestWithSkipStep(HttpRunner):

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
            .extract()
            .with_jmespath("body.args.foo2", "foo3")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.args.foo1", "bar11")
            .assert_equal("body.args.sum_v", "3")
            .assert_equal("body.args.foo2", "bar21")
        ),
        Step(
            RunRequest("skip this step with skip_if")
            .skip_if("'$foo3'=='bar21'", "reason 2021")
            .post("/post")
            .with_headers(
                **{
                    "User-Agent": "HttpRunner/${get_httprunner_version()}",
                    "Content-Type": "text/plain",
                }
            )
            .with_data(
                "This is expected to be sent back as part of response body: $foo1-$foo2-$foo3."
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("run this step with skip_if")
            .skip_if("'$foo3'!='bar21'", "reason 2021")
            .post("/post")
            .with_headers(
                **{
                    "User-Agent": "HttpRunner/${get_httprunner_version()}",
                    "Content-Type": "text/plain",
                }
            )
            .with_data(
                "This is expected to be sent back as part of response body: $foo1-$foo2-$foo3."
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("run this step with skip_unless")
            .skip_unless("'$foo3'=='bar21'", "reason 2021")
            .post("/post")
            .with_headers(
                **{
                    "User-Agent": "HttpRunner/${get_httprunner_version()}",
                    "Content-Type": "text/plain",
                }
            )
            .with_data(
                "This is expected to be sent back as part of response body: $foo1-$foo2-$foo3."
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("skip this step with skip_unless")
            .skip_unless("'$foo3'!='bar21'", "reason 2021")
            .post("/post")
            .with_headers(
                **{
                    "User-Agent": "HttpRunner/${get_httprunner_version()}",
                    "Content-Type": "text/plain",
                }
            )
            .with_data(
                "This is expected to be sent back as part of response body: $foo1-$foo2-$foo3."
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
    ]


if __name__ == "__main__":
    TestCaseRequestWithSkipStep().test_start()
