import datetime

import pytest

from httprunner import HttpRunner, Config, Step, RunRequest


@pytest.mark.meta(author="Raigor Deng")
class TestRunRequest(HttpRunner):
    config = (
        Config("test pre post delay")
        .base_url("https://postman-echo.com")
        .verify(False)
        .variables(
            **{
                "datetime": datetime,
                "delay": 1,
                "config_parse_time": "${pyexp(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())}",
            }
        )
    )

    teststeps = [
        Step(
            RunRequest("pre delay")
            .parametrize("parametrize_delay", ["$delay", "${pyexp(delay * 2)}"])
            .with_pre_delay("$delay")
            .post("/post")
            .with_json(
                {
                    "config_parse_time": "$config_parse_time",
                    "step_parse_time": "${pyexp(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())}",
                }
            )
            .extract()
            .with_jmespath("body.json.step_parse_time", "step_parse_time")
            .validate()
            .assert_greater_than(
                (
                    "${pyexp("
                    "(datetime.datetime.fromisoformat(step_parse_time) - "
                    "datetime.datetime.fromisoformat(config_parse_time))"
                    ".total_seconds()"
                    ")}"
                ),
                "$parametrize_delay",
            )
        ),
    ]
