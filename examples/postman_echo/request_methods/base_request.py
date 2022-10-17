from httprunner import HttpRunner, Config, Step, RunRequest


class TestCaseRequestAndExport(HttpRunner):

    config = (
        Config("request and export")
        .variables(
            **{
                "key01": 1,
                "key02": "value02",
                "key03": [1, 2, 3],
                "key04": {"foo": "bar"},
                "key05": "value",
            }
        )
        .base_url("https://postman-echo.com")
        .verify(False)
        .export(*["v01", "v02", "v03", "v04", "v"])
    )

    teststeps = [
        Step(
            RunRequest("post with json")
            .post("/post")
            .with_json(
                {
                    "key01": "$key01",
                    "key02": "$key02",
                    "key03": "$key03",
                    "key04": "$key04",
                }
            )
            .extract()
            .with_jmespath("body.json.key01", "v01")
            .with_jmespath("body.json.key02", "v02")
            .with_jmespath("body.json.key03", "v03")
            .with_jmespath("body.json.key04", "v04")
            .export()
            .variable("key05", "v")
            .validate()
            .assert_equal("status_code", 200)
        ),
    ]
