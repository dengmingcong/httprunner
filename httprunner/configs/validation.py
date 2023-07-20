from pydantic import BaseSettings


class ContentKeys(BaseSettings):
    """Settings for validation result keys."""

    result: str = "Result"
    assert_: str = "Assert"
    actual_value: str = "ActualValue"
    comparator: str = "Comparator"
    expect_value: str = "ExpectValue"
    message: str = "Message"
    jmespath_: str = "JMESPath"
    raw_expect_value: str = "RawExpectValue"

    class Config:
        env_prefix = "httprunner_validation_"


class Content(BaseSettings):
    keys: ContentKeys = ContentKeys()

    class Config:
        env_prefix = "httprunner_validation_"


class ValidationSettings(BaseSettings):
    """Settings for validation."""

    content: Content = Content()

    class Config:
        env_prefix = "httprunner_validation_"


validation_settings = ValidationSettings()
