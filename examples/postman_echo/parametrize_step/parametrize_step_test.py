from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class SubTestCase(HttpRunner):
    config = Config("base case with parametrized steps").base_url(
        "https://www.postman-echo.com"
    )
    teststeps = [
        Step(
            RunRequest("sub parametrized step")
            .parametrize("bar", ["a", "b"])
            .post("/post")
            .with_json(
                {
                    "foo": "$foo",
                    "bar": "$bar",
                }
            )
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
    ]


class TestParametrizeStep(HttpRunner):
    config = (
        Config("test parametrizing steps")
        .base_url("https://www.postman-echo.com")
        .variables(**{"sum_v": 0})
    )
    teststeps = [
        Step(
            RunRequest("parametrize in RunRequest")
            .parametrize("foo,bar", [(1, 1), (2, 2)])
            .post("/post")
            .with_json({"foo": "$foo", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
        Step(
            RunTestCase("parametrize in RunTestCase")
            .parametrize("foo,bar", [(1, 1), (2, 2)])
            .call(SubTestCase)
        ),
        Step(
            RunRequest("id is a list")
            .parametrize("foo,bar", [(1, 1), (2, 2)], [1, 2])
            .post("/post")
            .with_json({"foo": "$foo", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
        Step(
            RunRequest("parametrize and retry")
            .parametrize("foo,bar", [(1, 1), (2, 2)])
            .retry_on_failure(3, 0.5, is_relay_export=True)
            .get("/get")
            .with_params(**{"sum_v": "${sum_two($sum_v, $foo)}"})
            .with_headers(**{"User-Agent": "HttpRunner/${get_httprunner_version()}"})
            .extract()
            .with_jmespath("body.args.sum_v", "sum_v")
            .validate()
            .assert_equal("status_code", 200)
            .assert_greater_or_equals("body.args.sum_v", "4")
        ),
        Step(
            RunRequest("parametrize and skip")
            .parametrize("foo,bar", [(1, 1), (2, 2)])
            .skip_if("$foo == 2")
            .post("/post")
            .with_json({"foo": "$foo", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
        Step(
            RunRequest("parametrize with exported variables - extract")
            .post("/post")
            .with_json(
                {
                    "baz": "baz",
                }
            )
            .extract()
            .with_jmespath("body.json.baz", "baz")
        ),
        Step(
            RunRequest("parametrize with exported variables - use export variables")
            .parametrize("baz", ["$baz", "another_baz"])
            .post("/post")
            .with_json(
                {
                    "baz": "$baz",
                }
            )
            .validate()
            .assert_equal("body.json.baz", "$baz")
        ),
        Step(
            RunRequest(
                "step.variables would not be parsed until expanded steps were executed"
            )
            .parametrize("foo,bar", [(1, 1), (2, 2)])
            .with_variables(**{"baz": "$foo"})
            .post("/post")
            .with_json({"foo": "$baz", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
        Step(
            RunRequest("value of variable is a dict")
            .parametrize("foo,bar", [(1, 1), (2, 2)])
            .with_variables(**{"baz": {"foo": "$foo"}})
            .post("/post")
            .with_json({"foo": "$baz", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
        Step(
            RunRequest("is_skip_empty_parameter is True")
            .parametrize("foo,bar", [])
            .with_variables(**{"baz": {"foo": "$foo"}})
            .post("/post")
            .with_json({"foo": "$baz", "bar": "$bar"})
            .validate()
            .assert_equal("body.json.foo.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
    ]
