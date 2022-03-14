from httprunner import HttpRunner, Config, Step, RunRequest


class TestCaseUpdateJson(HttpRunner):

    config = (
        Config("test update json")
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
            .update_json_object({
                "foo": "$foo",
                "bar": "$bar"
            })
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
        Step(
            RunRequest("with_json has been called")
            .post("/post")
            .with_json({
                "foo": 3,
                "baz": "$baz"
            })
            .update_json_object({
                "foo": "$foo",
                "bar": "$bar"
            })
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
            .assert_equal("body.json.baz", "$baz")
        ),
    ]


if __name__ == "__main__":
    TestCaseUpdateJson().test_start()
