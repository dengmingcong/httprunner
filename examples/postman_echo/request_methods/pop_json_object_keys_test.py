from httprunner import HttpRunner, Config, Step, RunRequest


class TestCasePopJsonObjectKeys(HttpRunner):

    config = (
        Config("test pop json object keys")
        .variables(**{
            "foo": 1,
            "bar": 2,
            "baz": 3
        })
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("with_json has not been called")
            .post("/post")
            .with_json({
                "foo": "$foo",
                "bar": "$bar"
            })
            .pop_json_object_keys("foo")
            .validate()
            .assert_equal("body.json.bar", "$bar")
        ),
    ]


if __name__ == "__main__":
    TestCasePopJsonObjectKeys().test_start()
