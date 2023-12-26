import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


class BasePost(HttpRunner):

    config = Config("base post").base_url("https://postman-echo.com").verify(False)

    teststeps = [
        Step(
            RunRequest("")
            .post("/post")
            .with_data("foo-bar")
            .validate()
            .assert_equal("status_code", 300)
        )
    ]


@pytest.fixture(autouse=True)
def bad_post():
    (BasePost().run())


@pytest.mark.nosummary
@pytest.mark.xfail(raises=ValidationFailure)
class TestFixtureFailFast(HttpRunner):

    config = (
        Config("fixture will fail fast")
        .continue_on_failure()
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("")
            .post("/post")
            .with_data("foo-bar")
            .validate()
            .assert_equal("status_code", 200)
        )
    ]
