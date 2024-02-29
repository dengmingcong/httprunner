import pytest

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


@pytest.mark.meta(author="Raigor Deng")
class TestEachItemEqual(HttpRunner):
    config = (
        Config("test each item equal")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("test each item equal")
            .post("/post")
            .with_json(
                {
                    "products": [
                        {"name": "apple", "price": 1, "category": "fruit"},
                        {"name": "banana", "price": 2, "category": "fruit"},
                    ]
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_each_equal("body.json.products.map(&category, @)", "fruit")
        )
    ]


@pytest.mark.xfail(raises=ValidationFailure)
@pytest.mark.meta(author="Raigor Deng")
class TestEmptyList(HttpRunner):
    config = (
        Config("test empty list").base_url("https://postman-echo.com").verify(False)
    )

    teststeps = [
        Step(
            RunRequest("test empty list")
            .post("/post")
            .with_json({"products": []})
            .validate()
            .assert_equal("status_code", 200)
            .assert_each_equal("body.json.products.map(&category, @)", "fruit")
        )
    ]


@pytest.mark.xfail(raises=ValidationFailure)
@pytest.mark.meta(author="Raigor Deng")
class TestSomeItemsNotEqual(HttpRunner):
    config = (
        Config("test some items not equal")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("test some items not equal")
            .post("/post")
            .with_json(
                {
                    "products": [
                        {"name": "apple", "price": 1, "category": "fruit"},
                        {"name": "banana", "price": 2, "category": "fruit"},
                        {"name": "carrot", "price": 3, "category": "vegetable"},
                    ]
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_each_equal("body.json.products.map(&category, @)", "fruit")
        )
    ]
