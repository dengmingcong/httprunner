from pydantic import BaseSettings


class ResultDictIcons(BaseSettings):
    pass_: str = "✔️"
    fail: str = "❌"


class ResultDictKeys(BaseSettings):
    """Settings for validation result keys."""
    result: str = "Result"
    assert_: str = "Assert"
    actual_value: str = "ActualValue"
    comparator: str = "Comparator"
    expect_value: str = "ExpectValue"
    message: str = "Message"
    jmespath_: str = "JMESPath"
    raw_expect_value: str = "RawExpectValue"


class ResultAttachmentIcons(BaseSettings):
    pass_: str = "🟢"
    fail: str = "🔴"


class ResultDict(BaseSettings):
    keys: ResultDictKeys = ResultDictKeys()
    icons: ResultDictIcons = ResultDictIcons()


class ResultAttachment(BaseSettings):
    icons: ResultAttachmentIcons = ResultAttachmentIcons()


class Result(BaseSettings):
    dict_: ResultDict = ResultDict()
    attachment: ResultAttachment = ResultAttachment()


class ValidationSettings(BaseSettings):
    """Settings for validation."""
    result: Result = Result()
