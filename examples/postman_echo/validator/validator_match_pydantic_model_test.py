from pydantic import BaseModel, ConfigDict

from httprunner import HttpRunner, Config, Step, RunRequest


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


class TestValidatorMatchPydanticModel(HttpRunner):
    config = (
        Config("test validator match pydantic model")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("exactly match")
            .post("/post")
            .with_json(
                {
                    "configModel": "foo",
                    "modelName": "foo",
                    "alexaSupported": True,
                    "brand": {"name": "foo"},
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
            RunRequest("extra attribute")
            .post("/post")
            .with_json(
                {
                    "configModel": "foo",
                    "modelName": "foo",
                    "alexaSupported": True,
                    "extra": 1,
                    "brand": {"name": "foo"},
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_match_pydantic_model(
                "body.json",
                Sku,
            )
        ),
    ]
