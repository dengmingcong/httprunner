from httprunner import HttpRunner, Config, Step, RunRequest


class TestFailStepAlsoExportVars(HttpRunner):
    config = (
        Config("test fail step also export vars")
        .variables(**{"sum_v": 0})
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("fail step also export vars")
            .retry_on_failure(3, 0.5, is_relay_export=True)
            .get("/get")
            .with_params(**{"sum_v": "${sum_two($sum_v, 1)}"})
            .with_headers(**{"User-Agent": "HttpRunner/${get_httprunner_version()}"})
            .extract()
            .with_jmespath("body.args.sum_v", "sum_v")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.args.sum_v", "4")
        )
    ]
