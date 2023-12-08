import pytest
from pydantic import BaseModel, ConfigDict

from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner.exceptions import ValidationFailure


def snake_to_camel(snake_str: str, is_first_word_lower: bool = True) -> str:
    """
    Convert snake string to camel string.
    """
    components = snake_str.split("_")

    if is_first_word_lower:
        return components[0] + "".join(x.title() for x in components[1:])
    else:
        return "".join(x.title() for x in components)


class Brand(BaseModel):
    name: str


class Sku(BaseModel):
    config_model: str
    model_name: str
    alexa_supported: bool
    brand: Brand
    model_config = ConfigDict(alias_generator=snake_to_camel)


@pytest.mark.xfail(raises=ValidationFailure)
class TestValidatorMatchPydanticModel(HttpRunner):
    config = (
        Config("test validator match pydantic model")
        .base_url("https://postman-echo.com")
        .verify(False)
        .continue_on_failure()
    )

    teststeps = [
        Step(
            RunRequest("type not match")
            .post("/post")
            .with_json(
                {
                    "configModel": 1,
                    "modelName": 1,
                    "alexaSupported": "yes",
                    "brand": {"name": 1},
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_match_pydantic_model(
                "body.json",
                Sku,
            )
        ),
        Step(
            RunRequest("nested model not match")
            .post("/post")
            .with_json(
                {
                    "configModel": "foo",
                    "modelName": "foo",
                    "alexaSupported": True,
                    "brand": "foo",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_match_pydantic_model(
                "body.json",
                Sku,
            )
        ),
        Step(
            RunRequest("missing attribute")
            .post("/post")
            .with_json(
                {"configModel": "foo", "modelName": "foo", "brand": {"name": "foo"}}
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_match_pydantic_model(
                "body.json",
                Sku,
            )
        ),
    ]
