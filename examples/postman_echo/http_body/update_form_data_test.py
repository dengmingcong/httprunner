from httprunner import HttpRunner, Config, Step, RunRequest


class TestCaseUpdateFormData(HttpRunner):

    config = (
        Config("test update json")
        .variables(**{"foo": "1", "bar": "2", "baz": "3"})
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("with_data has been called")
            .post("/post")
            .with_data({"foo": "3", "baz": "$baz"})
            .update_form_data({"foo": "$foo", "bar": "$bar"})
            .validate()
            .assert_equal("body.form.foo", "$foo")
            .assert_equal("body.form.bar", "$bar")
            .assert_equal("body.form.baz", "$baz")
        ),
        Step(
            RunRequest("json set by variables")
            .with_variables(
                **{
                    "init_data": {"foo": "3", "baz": "$baz"},
                    "update_data": {"foo": "$foo", "bar": "$bar"},
                }
            )
            .post("/post")
            .with_data("$init_data")
            .update_form_data("$update_data")
            .validate()
            .assert_equal("body.form.foo", "1")
            .assert_equal("body.form.bar", "2")
            .assert_equal("body.form.baz", "3")
        ),
    ]


if __name__ == "__main__":
    TestCaseUpdateFormData().test_start()
