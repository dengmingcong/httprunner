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
                "delay": 5,
                "before_post_delay": "${pyexp(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())}",
            }
        )
    )

    teststeps = [
        Step(
            RunRequest("post delay")
            .skip_if(True)
            .with_post_delay("$delay")
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
            .assert_less_than(
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
