import datetime

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.testcase import HttpRunnerRequest, RequestConfig


class Base(HttpRunnerRequest):
    config = RequestConfig("default name")
    request = RunRequest("").post("/post")


class TestDelay(HttpRunner):
    config = (
        Config("test delay")
        .base_url("https://postman-echo.com")
        .variables(
            **{
                "datetime": datetime,
                "delay": 1,
                "config_parse_time": "${pyexp(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())}",
            }
        )
        .verify(False)
    )

    teststeps = [
        Step(
            Base("pre delay")
            .with_pre_delay("$delay")
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
        Step(Base("post delay").with_post_delay("$delay")),
        Step(
            Base("request after post delay")
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
