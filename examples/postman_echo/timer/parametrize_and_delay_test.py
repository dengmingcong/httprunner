import datetime

import pytest

from httprunner import HttpRunner, Config, Step, RunRequest


@pytest.mark.meta(author="Raigor Deng")
class TestRunRequest(HttpRunner):
    config = (
        Config("test pre post delay")
        .base_url("https://postman-echo.com")
        .verify(False)
        .variables(**{"datetime": datetime, "delay": 1})
    )

    teststeps = [
        Step(
            RunRequest("pre delay")
            .parametrize("parametrize_delay", ["$delay", "${pyexp(delay * 2)}"])
            .with_pre_delay("$delay")
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
            .validate()
            .assert_greater_than(
                (
                    "${pyexp("
                    "(datetime.datetime.fromisoformat(parse_time) - datetime.datetime.fromisoformat(import_time))"
                    ".total_seconds()"
                    ")}"
                ),
                "$parametrize_delay",
            )
        ),
    ]
