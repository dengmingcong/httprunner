from httprunner import HttpRunner, Config, Step, RunRequest


class TestValidatorMatchSchema(HttpRunner):
    config = (
        Config("test validator match schema")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("instance match schema")
            .post("/post")
            .with_json({"name": "Eggs", "price": 34.99})
            .validate()
            .assert_equal("status_code", 200)
            .assert_match_json_schema(
                "body.json",
                {
                    "type": "object",
                    "properties": {
                        "price": {"type": "number"},
                        "name": {"type": "string"},
                    },
                },
            )
        ),
    ]
