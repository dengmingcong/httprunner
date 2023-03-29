from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class SubTestCase(HttpRunner):
    config = Config("base case with parametrized steps").base_url("https://www.postman-echo.com")
    teststeps = [
        Step(
            RunRequest("sub parametrized step")
            .parametrize("bar", ["a", "b"])
            .post("/post")
            .with_json({
                "foo": "$foo",
                "bar": "$bar",
            })
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
    ]


class TestParametrizeStep(HttpRunner):
    config = Config("test parametrizing steps").base_url("https://www.postman-echo.com")
    teststeps = [
        Step(
            RunRequest("parametrize in RunRequest")
            .parametrize("foo,bar", [(1, 1), (2, 2)])
            .post("/post")
            .with_json({
                "foo": "$foo",
                "bar": "$bar"
            })
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
            .with_json({
                "foo": "$foo",
                "bar": "$bar"
            })
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
        Step(
            RunRequest("parametrize and retry")
            .parametrize("foo,bar", [(1, 1), (2, 2)])
            .with_variables(**{
                "sum_v": 0
            })
            .retry_on_failure(3, 0.5)
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
            .with_json({
                "foo": "$foo",
                "bar": "$bar"
            })
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
    ]
