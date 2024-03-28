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
            .parametrize("foo,bar", [(1, 1), (2, 2)], is_keep_export_history=True)
            .call(SubTestCase)
            .export(*["foo", "bar"])
        ),
        Step(
            RunTestCase("parametrize in RunTestCase")
            .parametrize("foo,bar", [(3, 4), (5, 6)], is_keep_export_history=True)
            .call(SubTestCase)
            .export(foo="foo_alias", bar="bar_alias")
        ),
        Step(
            RunRequest("parametrize in RunRequest with exported variables")
            .parametrize("foo,bar", [("$foo_0", "$bar_0"), ("$foo_1", "$bar_1")])
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
            .with_json({"baz": ["$foo_0", "$foo_0", "$bar_1", "$bar_1"]})
            .validate()
            .assert_length_equal("body.json.baz", 4)
        ),
    ]
