from httprunner import HttpRunner, Config, Step, RunRequest


class TestCaseUpdateUrlOrigin(HttpRunner):

    config = (
        Config("test update url origin")
        .variables(**{"foo": 1, "bar": 2, "baz": 3})
        .base_url("http://bad-netloc.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("update origin")
            .post("/post")
            .with_origin("https://postman-echo.com")
            .with_json({"foo": "$foo", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
        Step(
            RunRequest("don't update origin")
            .post("https://postman-echo.com/post")
            .with_json({"foo": "$foo", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
    ]


if __name__ == "__main__":
    TestCaseUpdateUrlOrigin().test_start()
