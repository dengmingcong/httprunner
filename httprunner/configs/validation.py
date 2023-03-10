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


class Content(BaseSettings):
    keys: ContentKeys = ContentKeys()


class ValidationSettings(BaseSettings):
    """Settings for validation."""
    content: Content = Content()


validation_settings = ValidationSettings()
