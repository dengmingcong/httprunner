from pydantic_settings import BaseSettings, SettingsConfigDict


class ContentKeys(BaseSettings):
    """Settings for validation result keys."""

    result: str = "Result"
    assert_: str = "Assert"
    actual_value: str = "ActualValue"
    comparator: str = "Comparator"
    expect_value: str = "ExpectValue"
    message: str = "Message"
    validator_config: str = "ValidatorConfig"
    jmespath_: str = "JMESPath"
    raw_expect_value: str = "RawExpectValue"
    model_config = SettingsConfigDict(env_prefix="httprunner_validation_")


class Content(BaseSettings):
    keys: ContentKeys = ContentKeys()
    model_config = SettingsConfigDict(env_prefix="httprunner_validation_")


class ValidationSettings(BaseSettings):
    """Settings for validation."""

    content: Content = Content()
    model_config = SettingsConfigDict(env_prefix="httprunner_validation_")


validation_settings = ValidationSettings()
