import datetime

import pytest

from httprunner import Config, HttpRunner, RunRequest, Step


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
            .with_pre_delay("$delay", "pre delay reason")
            .post("/post")
            .with_json(
                {
                    "config_parse_time": "$config_parse_time",
                    "step_parse_time": "${pyexp(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())}",
                }
            )
            .extract()
            .with_jmespath("body.json.step_parse_time", "step_parse_time")
            .export()
            .variable("step_parse_time", "before_post_delay")
            .validate()
            .assert_greater_than(
                (
                    "${pyexp("
                    "(datetime.datetime.fromisoformat(step_parse_time) - "
                    "datetime.datetime.fromisoformat(config_parse_time))"
                    ".total_seconds()"
                    ")}"
                ),
                "$delay",
            )
        ),
        Step(
            RunRequest("post delay")
            .with_post_delay("$delay", "post delay reason")
            .post("/post")
        ),
        Step(
            RunRequest("request after post delay")
            .post("/post")
            .with_json(
                {
                    "after_post_delay": "${pyexp(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())}",
                }
            )
            .extract()
            .with_jmespath("body.json.after_post_delay", "after_post_delay")
            .validate()
            .assert_greater_than(
                (
                    "${pyexp("
                    "(datetime.datetime.fromisoformat(after_post_delay) - "
                    "datetime.datetime.fromisoformat(before_post_delay))"
                    ".total_seconds()"
                    ")}"
                ),
                "$delay",
            )
        ),
    ]
