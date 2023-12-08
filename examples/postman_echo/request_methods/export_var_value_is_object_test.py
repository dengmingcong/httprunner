from httprunner import HttpRunner, Config, Step, RunRequest


class TestCaseExportVarValueIsObject(HttpRunner):

    config = (
        Config("test extracted variable's value is object")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("export value is object")
            .with_variables(**{"obj": object()})
            .post("/post")
            .with_json(
                {
                    "foo": "foo:1",
                }
            )
            .export()
            .variable("obj")
        ),
    ]
