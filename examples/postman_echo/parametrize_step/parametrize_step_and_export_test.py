from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class SubTestCase(HttpRunner):
    config = (
        Config("base case with parametrized steps")
        .base_url("https://www.postman-echo.com")
        .export(*["foo", "bar"])
    )
    teststeps = [
        Step(
            RunRequest("sub parametrized step")
            # .parametrize("bar", ["a", "b"])
            .post("/post")
            .with_json(
                {
                    "foo": "$foo",
                    "bar": "$bar",
                }
            )
            .extract()
            .with_jmespath("body.json.foo", "foo")
            .with_jmespath("body.json.bar", "bar")
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
            RunTestCase("parametrize in RunTestCase")
            .parametrize("foo,bar", [(1, 1), (2, 2)])
            .call(SubTestCase)
            .export(foo="foo1", *["foo", "bar"])
        ),
        Step(
            RunRequest("parametrize in RunRequest with exported variables")
            .parametrize("foo,bar", [("$foo_1", "$bar_1"), ("$foo_2", "$bar_2")])
            .post("/post")
            .with_json({"foo": "$foo", "bar": "$bar"})
            .extract()
            .with_jmespath("body.json.foo", "foo")
            .with_jmespath("body.json.bar", "bar")
            .validate()
            .assert_equal("body.json.foo", "$foo")
            .assert_equal("body.json.bar", "$bar")
        ),
        Step(
            RunRequest("parametrize with exported variables - extract")
            .post("/post")
            .with_json({"baz": ["$foo_1", "$foo_2", "$bar_1", "$bar_2"]})
            .validate()
            .assert_length_equal("body.json.baz", 4)
        ),
    ]
