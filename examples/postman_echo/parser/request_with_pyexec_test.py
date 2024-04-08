from httprunner import Config, HttpRunner, RunRequest, Step


class Baz:
    def __init__(self, value):
        self.value = value


class TestPyexec(HttpRunner):
    config = (
        Config("test pyexec")
        .variables(
            **{
                "foo": 1,
                "bar": 2,
                "no_return": "${pyexec(baz.value = 4)}",
                "baz": Baz(3),
            }
        )
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("change baz's attribute `value` with pyexec")
            .post("/post")
            .with_json(
                {
                    "sum": "${pyexp(foo + bar)}",
                    "app_version": "${pyexp(get_app_version()[0])}",
                    "baz_value": "${baz.value}",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.sum", 3)
            .assert_equal("body.json.baz_value", 4)
            .assert_equal("body.json.app_version", 3.1)
        ),
    ]
