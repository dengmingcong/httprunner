from httprunner import Config, HttpRunner, RunRequest, Step


class TestResponseIsNull(HttpRunner):
    config = (
        Config("test response is null")
        .base_url("https://test-online.vesync.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("post to api that will return null response")
            .post("/cloud/v1/updateEmailSubscribe")
            .with_json(
                {
                    "language": "EN",
                    "subscribeToken": "8d572c4c056ecd9aaf6399e62307920f",
                    "email": "raigordeng01@126.com",
                    "unsubscribeClassIdList": [],
                }
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
    ]
