from pydantic import BaseSettings


class ContentIcons(BaseSettings):
    pass_: str = "✔️"
    fail: str = "❌"


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


class AttachmentIcons(BaseSettings):
    pass_: str = "🟢"
    fail: str = "🔴"


class Content(BaseSettings):
    keys: ContentKeys = ContentKeys()
    icons: ContentIcons = ContentIcons()


class Attachment(BaseSettings):
    icons: AttachmentIcons = AttachmentIcons()


class ValidationSettings(BaseSettings):
    """Settings for validation."""
    content: Content = Content()
    attachment: Attachment = Attachment()


validation_settings = ValidationSettings()
