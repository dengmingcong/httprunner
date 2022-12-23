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
        Step(
            RunRequest("test deep is True")
            .post("/post")
            .with_json({
                "data": {
                    "foo": 3,
                    "baz": "$baz"
                }
            })
            .update_json_object({
                "data": {
                    "foo": "$foo",
                    "bar": "$bar"
                }
            })
            .validate()
            .assert_equal("body.json.data.foo", "$foo")
            .assert_equal("body.json.data.bar", "$bar")
            .assert_equal("body.json.data.baz", "$baz")
        ),
        Step(
            RunRequest("test deep is False")
            .post("/post")
            .with_json({
                "data": {
                    "foo": 3,
                    "baz": "$baz"
                }
            })
            .update_json_object({
                "data": {
                    "foo": "$foo",
                    "bar": "$bar"
                }
            }, False)
            .validate()
            .assert_equal("body.json.data.foo", "$foo")
            .assert_equal("body.json.data.bar", "$bar")
            .assert_equal("body.json.data.baz", None)
        ),
        Step(
            RunRequest("set json and json_update with variable")
            .with_variables(**{
                "init_json": {
                    "data": {
                        "foo": 3,
                        "baz": "$baz"
                    }
                },
                "update_json": {
                    "data": {
                        "foo": "$foo",
                        "bar": "$bar"
                    }
                }
            })
            .post("/post")
            .with_json("$init_json")
            .update_json_object("$update_json", True)
            .validate()
            .assert_equal("body.json.data.foo", 1)
            .assert_equal("body.json.data.bar", 2)
            .assert_equal("body.json.data.baz", 3)
        ),
        Step(
            RunRequest("set json and json_update with debugtalk")
            .post("/post")
            .with_json("${get_json(1, 2)}")
            .update_json_object("${get_json(3, 4)}", True)
            .validate()
            .assert_equal("body.json.foo", 3)
            .assert_equal("body.json.bar", 4)
        ),
        Step(
            RunRequest("update_json_object should be applied if with_json is a dict")
            .post("/post")
            .with_json({
                "foo": "$FAKE_VAR"
            })
            .update_json_object({
                "foo": 3
            }, True)
            .validate()
            .assert_equal("body.json.foo", 3)
        ),
    ]


if __name__ == "__main__":
    TestCaseUpdateJson().test_start()
