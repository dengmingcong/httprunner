from pydantic_settings import BaseSettings, SettingsConfigDict


class MockSettings(BaseSettings):
    """
    Settings for localization (shorted as l10n).
    """

    is_enabled: bool = False
    model_config = SettingsConfigDict(env_prefix="mock_")


mock_settings = MockSettings()
