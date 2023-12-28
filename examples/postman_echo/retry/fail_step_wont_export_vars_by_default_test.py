import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


@pytest.mark.xfail(raises=ValidationFailure)
class TestFailStepWillNotExportVars(HttpRunner):
    config = (
        Config("test fail step will not export vars")
        .variables(**{"sum_v": 0})
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("fail step will not export vars")
            .retry_on_failure(3, 0.5)
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
