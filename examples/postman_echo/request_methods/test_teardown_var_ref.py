from httprunner import Config, Step, HttpRunner, RunRequest


class TestReferPreStepTeardownHookVar(HttpRunner):

    config = (
        Config("test step refer to vars returned by teardown hook of previous step")
        .variables(api_name="connect")
        .base_url("https://postman-echo.com")
    )

    teststeps = [
        Step(
            RunRequest("first step")
            .get("/get")
            .with_json(
                {
                    "name": "${get_api_by_name($api_name)}"
                }
            )
            .teardown_hook("${get_name($response)}", "name")
            .extract()
            .validate()
            .assert_equal("body.args.name", "$name")
        ),
        Step(
            RunRequest("second step")
            .get("/get")
            .with_params(**{"name": "$name"})
        )
    ]


if __name__ == "__main__":
    TestReferPreStepTeardownHookVar().test_start()
