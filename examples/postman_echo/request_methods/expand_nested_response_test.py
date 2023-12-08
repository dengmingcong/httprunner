from httprunner import HttpRunner, Config, Step, RunRequest


class TestExpandResponseNestedJson(HttpRunner):
    config = (
        Config("expand response nested json")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest(
                "request with header X-Json-Control: expand, body contain Chinese chars"
            )
            .post("/post")
            .with_headers(**{"X-Json-Control": "expand"})
            .with_json(
                {
                    "int": 100,
                    "float": 100.02,
                    "str": "some string",
                    "strWithChinese": "我是中文",
                    "dict": {"foo": "foo"},
                    "dictWithList": {
                        "bar": [
                            {
                                "nest": '{"a":"中文","b":"b"}',
                            }
                        ]
                    },
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.dictWithList.bar[0].nest", {"a": "中文", "b": "b"})
        ),
        Step(
            RunRequest("request with header X-Json-Control: not-expand")
            .post("/post")
            .with_headers(**{"X-Json-Control": "not-expand"})
            .with_json(
                {
                    "dictWithList": {
                        "bar": [
                            {
                                "nest": '{"a":"中文","b":"b"}',
                            }
                        ]
                    }
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.dictWithList.bar[0].nest", '{"a":"中文","b":"b"}')
        ),
        Step(
            RunRequest(
                "request with header `x-json-control: expand` (case sensitive, all lowercase will not take effect)"
            )
            .post("/post")
            .with_headers(**{"x-json-control": "expand"})
            .with_json(
                {
                    "dictWithList": {
                        "bar": [
                            {
                                "nest": '{"a":"中文","b":"b"}',
                            }
                        ]
                    }
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.dictWithList.bar[0].nest", '{"a":"中文","b":"b"}')
        ),
        Step(
            RunRequest("request without header X-Json-Control")
            .post("/post")
            .with_json(
                {
                    "dictWithList": {
                        "bar": [
                            {
                                "nest": '{"a":"中文","b":"b"}',
                            }
                        ]
                    }
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.dictWithList.bar[0].nest", '{"a":"中文","b":"b"}')
        ),
    ]
