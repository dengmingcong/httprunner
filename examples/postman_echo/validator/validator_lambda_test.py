from httprunner import HttpRunner, Config, Step, RunRequest


def assert_value_is_bar(value):
    assert value == "bar"


def assert_value_plus_equal_three(value, addition: int):
    assert int(value) + addition == 3


class TestValidatorLambda(HttpRunner):

    config = (
        Config("test validator lambda")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("test validator lambda")
            .post("/post")
            .with_data({"foo": "bar"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_lambda("body.form.foo", assert_value_is_bar, "value is not bar")
        ),
        Step(
            RunRequest("test validator lambda with additional kwargs")
            .post("/post")
            .with_data({"foo": 1})
            .validate()
            .assert_equal("status_code", 200)
            .assert_lambda(
                "body.form.foo",
                assert_value_plus_equal_three,
                "value is not 1",
                validator_kwargs={"addition": 2},
            )
            .assert_lambda(
                "body.form.foo",
                (assert_value_plus_equal_three, {"addition": 2}),
                "value is not 1",
            )
        ),
    ]
