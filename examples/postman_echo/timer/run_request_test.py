import datetime

import pytest

from httprunner import HttpRunner, Config, Step, RunRequest


@pytest.mark.meta(author="Raigor Deng")
class TestRunRequest(HttpRunner):
    config = (
        Config("test pre post delay")
        .base_url("https://postman-echo.com")
        .verify(False)
        .variables(**{"datetime": datetime})
    )

    teststeps = [
        Step(
            RunRequest("pre delay")
            .with_pre_delay(1)
            .post("/post")
            .with_json(
                {
                    "import_time": datetime.datetime.now(
                        tz=datetime.timezone.utc
                    ).isoformat(),
                    "parse_time": "${pyexp(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())}",
                }
            )
            .extract()
            .with_jmespath("body.json.import_time", "import_time")
            .with_jmespath("body.json.parse_time", "parse_time")
            .export()
            .variable("parse_time", "before_post_delay")
            .validate()
            .assert_greater_than(
                (
                    "${pyexp("
                    "(datetime.datetime.fromisoformat(parse_time) - datetime.datetime.fromisoformat(import_time))"
                    ".total_seconds()"
                    ")}"
                ),
                1,
            )
        ),
        Step(RunRequest("post delay").with_post_delay(1).post("/post")),
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
                1,
            )
        ),
    ]
